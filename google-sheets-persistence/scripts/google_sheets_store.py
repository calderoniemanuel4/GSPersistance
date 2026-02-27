#!/usr/bin/env python3
"""Google Sheets persistence helper for Python agents."""

from __future__ import annotations

import argparse
import json
import logging
import os
from dataclasses import dataclass
from typing import Any

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependencies. Install with: pip install gspread google-auth"
    ) from exc

LOGGER = logging.getLogger("google_sheets_store")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


@dataclass(frozen=True)
class GoogleSheetsSettings:
    """Runtime settings for Google Sheets integration."""

    credentials_path: str
    spreadsheet_id: str
    worksheet_name: str
    key_column: str = "id"

    @classmethod
    def from_env(cls) -> "GoogleSheetsSettings":
        """Build settings from environment variables."""
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
        spreadsheet_id = os.getenv("GSHEETS_SPREADSHEET_ID", "").strip()
        worksheet_name = os.getenv("GSHEETS_WORKSHEET", "").strip()
        key_column = os.getenv("GSHEETS_KEY_COLUMN", "id").strip() or "id"

        missing = [
            name
            for name, value in (
                ("GOOGLE_APPLICATION_CREDENTIALS", credentials_path),
                ("GSHEETS_SPREADSHEET_ID", spreadsheet_id),
                ("GSHEETS_WORKSHEET", worksheet_name),
            )
            if not value
        ]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return cls(
            credentials_path=credentials_path,
            spreadsheet_id=spreadsheet_id,
            worksheet_name=worksheet_name,
            key_column=key_column,
        )


class GoogleSheetsStore:
    """High-level CRUD wrapper over a single Google Sheets worksheet."""

    def __init__(self, worksheet: gspread.Worksheet, key_column: str = "id") -> None:
        self._worksheet = worksheet
        self._key_column = key_column

    @classmethod
    def from_service_account_file(cls, settings: GoogleSheetsSettings) -> "GoogleSheetsStore":
        """Create store from service account file and sheet metadata."""
        credentials = Credentials.from_service_account_file(
            settings.credentials_path, scopes=SCOPES
        )
        client = gspread.authorize(credentials)
        spreadsheet = client.open_by_key(settings.spreadsheet_id)
        worksheet = spreadsheet.worksheet(settings.worksheet_name)
        return cls(worksheet=worksheet, key_column=settings.key_column)

    def ensure_headers(self, headers: list[str]) -> list[str]:
        """Ensure headers exist in row 1 and return resulting header order."""
        if self._key_column not in headers:
            headers = [self._key_column, *headers]

        current_headers = self._worksheet.row_values(1)
        if not current_headers:
            self._worksheet.update("1:1", [headers])
            return headers

        merged_headers = list(current_headers)
        for header in headers:
            if header not in merged_headers:
                merged_headers.append(header)

        if merged_headers != current_headers:
            self._worksheet.update("1:1", [merged_headers])
        return merged_headers

    def list_records(self, limit: int | None = None) -> list[dict[str, str]]:
        """Return records as dictionaries keyed by headers."""
        records = self._worksheet.get_all_records(expected_headers=self._worksheet.row_values(1))
        normalized = [{str(k): str(v) if v is not None else "" for k, v in row.items()} for row in records]
        return normalized if limit is None else normalized[:limit]

    def get_record(self, key: str) -> dict[str, str] | None:
        """Get one record by key column value."""
        row_index = self._find_row_by_key(key)
        if row_index is None:
            return None

        headers = self._worksheet.row_values(1)
        values = self._worksheet.row_values(row_index)
        padded = values + [""] * (len(headers) - len(values))
        return dict(zip(headers, padded, strict=True))

    def upsert_record(self, key: str, record: dict[str, Any]) -> None:
        """Insert or update a record identified by key."""
        payload = {str(k): "" if v is None else str(v) for k, v in record.items()}
        payload[self._key_column] = key

        headers = self.ensure_headers(list(payload.keys()))
        row_values = [payload.get(header, "") for header in headers]
        row_index = self._find_row_by_key(key)

        if row_index is None:
            self._worksheet.append_row(row_values, value_input_option="USER_ENTERED")
            return
        self._worksheet.update(f"A{row_index}", [row_values], value_input_option="USER_ENTERED")

    def delete_record(self, key: str) -> bool:
        """Delete one record by key. Return True if deleted."""
        row_index = self._find_row_by_key(key)
        if row_index is None:
            return False
        self._worksheet.delete_rows(row_index)
        return True

    def _find_row_by_key(self, key: str) -> int | None:
        """Find row index (1-based) for key value. Header row is excluded."""
        headers = self._worksheet.row_values(1)
        if not headers:
            return None
        if self._key_column not in headers:
            raise ValueError(
                f"Key column '{self._key_column}' not found. Call ensure_headers first."
            )

        key_col_index = headers.index(self._key_column) + 1
        values = self._worksheet.col_values(key_col_index)
        for idx, value in enumerate(values[1:], start=2):
            if value == key:
                return idx
        return None


def _parse_json_record(value: str) -> dict[str, Any]:
    """Parse JSON text into dictionary payload."""
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in --record: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("--record must be a JSON object")
    return parsed


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Google Sheets persistence CLI")
    parser.add_argument("--log-level", default="INFO", help="Logging level (INFO, DEBUG, ...)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ensure_headers = subparsers.add_parser("ensure-headers", help="Ensure header row exists")
    ensure_headers.add_argument("--headers", required=True, help="Comma-separated headers")

    get_cmd = subparsers.add_parser("get", help="Get one record by key")
    get_cmd.add_argument("--key", required=True, help="Unique row key")

    upsert_cmd = subparsers.add_parser("upsert", help="Insert/update one record by key")
    upsert_cmd.add_argument("--key", required=True, help="Unique row key")
    upsert_cmd.add_argument("--record", required=True, help='JSON object, e.g. \'{"status":"ok"}\'')

    list_cmd = subparsers.add_parser("list", help="List records")
    list_cmd.add_argument("--limit", type=int, default=None, help="Optional max rows")

    delete_cmd = subparsers.add_parser("delete", help="Delete one record by key")
    delete_cmd.add_argument("--key", required=True, help="Unique row key")
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level.upper(), format="%(levelname)s %(message)s")

    settings = GoogleSheetsSettings.from_env()
    store = GoogleSheetsStore.from_service_account_file(settings)

    if args.command == "ensure-headers":
        headers = [value.strip() for value in args.headers.split(",") if value.strip()]
        result = store.ensure_headers(headers)
        print(json.dumps({"headers": result}, ensure_ascii=True))
        return 0

    if args.command == "get":
        result = store.get_record(args.key)
        print(json.dumps({"record": result}, ensure_ascii=True))
        return 0

    if args.command == "upsert":
        payload = _parse_json_record(args.record)
        store.upsert_record(args.key, payload)
        print(json.dumps({"status": "ok", "key": args.key}, ensure_ascii=True))
        return 0

    if args.command == "list":
        rows = store.list_records(limit=args.limit)
        print(json.dumps({"records": rows, "count": len(rows)}, ensure_ascii=True))
        return 0

    if args.command == "delete":
        deleted = store.delete_record(args.key)
        print(json.dumps({"deleted": deleted, "key": args.key}, ensure_ascii=True))
        return 0

    LOGGER.error("Unsupported command: %s", args.command)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
