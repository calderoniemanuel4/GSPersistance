#!/usr/bin/env python3
"""Bootstrap and seed a Firestore database from the command line."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Any


DEFAULT_DATABASE_ID = "(default)"


@dataclass(frozen=True)
class FirestoreConfig:
    """Runtime configuration for the Firestore client."""

    project_id: str
    database_id: str = DEFAULT_DATABASE_ID


def build_config(project_id: str | None, database_id: str | None) -> FirestoreConfig:
    """Resolve configuration from CLI args and environment variables."""
    resolved_project_id = project_id or os.environ.get("FIRESTORE_PROJECT_ID")
    if not resolved_project_id:
        raise ValueError(
            "Missing project id. Pass --project-id or set FIRESTORE_PROJECT_ID."
        )

    resolved_database_id = database_id or os.environ.get(
        "FIRESTORE_DATABASE_ID", DEFAULT_DATABASE_ID
    )
    return FirestoreConfig(
        project_id=resolved_project_id,
        database_id=resolved_database_id,
    )


def get_firestore_client(config: FirestoreConfig):
    """Create and return a Firebase Admin Firestore client."""
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError as exc:
        raise RuntimeError(
            "firebase-admin is required. Install it with 'pip install firebase-admin'."
        ) from exc

    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path:
        raise ValueError(
            "Missing GOOGLE_APPLICATION_CREDENTIALS. Set it to the service account JSON path."
        )

    if not os.path.exists(cred_path):
        raise FileNotFoundError(
            f"Credential file does not exist: {cred_path}"
        )

    app_name = f"firestore-bootstrap:{config.project_id}:{config.database_id}"
    try:
        app = firebase_admin.get_app(app_name)
    except ValueError:
        app = firebase_admin.initialize_app(
            credentials.Certificate(cred_path),
            {"projectId": config.project_id},
            name=app_name,
        )

    return firestore.client(app=app, database_id=config.database_id)


def parse_json_payload(raw_payload: str) -> dict[str, Any]:
    """Parse a JSON object payload passed via CLI."""
    try:
        parsed = json.loads(raw_payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("The payload must be a JSON object.")

    return parsed


def seed_document(
    *,
    collection: str,
    document_id: str,
    payload: dict[str, Any],
    project_id: str | None,
    database_id: str | None,
    merge: bool,
) -> None:
    """Create or update a Firestore document."""
    config = build_config(project_id, database_id)
    client = get_firestore_client(config)
    doc_ref = client.collection(collection).document(document_id)
    doc_ref.set(payload, merge=merge)

    print(
        json.dumps(
            {
                "ok": True,
                "project_id": config.project_id,
                "database_id": config.database_id,
                "collection": collection,
                "document_id": document_id,
                "merge": merge,
            },
            indent=2,
        )
    )


def show_env(project_id: str | None, database_id: str | None) -> None:
    """Print the resolved environment without making a Firestore write."""
    config = build_config(project_id, database_id)
    print(
        json.dumps(
            {
                "project_id": config.project_id,
                "database_id": config.database_id,
                "credentials_path": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            },
            indent=2,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser."""
    parser = argparse.ArgumentParser(
        description="Bootstrap a Firestore database and seed a document."
    )
    parser.add_argument(
        "--project-id",
        help="Firestore project id. Falls back to FIRESTORE_PROJECT_ID.",
    )
    parser.add_argument(
        "--database-id",
        help="Firestore database id. Falls back to FIRESTORE_DATABASE_ID or (default).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    seed_parser = subparsers.add_parser(
        "seed",
        help="Create or update one document in Firestore.",
    )
    seed_parser.add_argument("--collection", required=True, help="Collection name.")
    seed_parser.add_argument("--document-id", required=True, help="Document id.")
    seed_parser.add_argument(
        "--data",
        required=True,
        help="JSON object to write into the document.",
    )
    seed_parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge with the existing document instead of replacing it.",
    )

    subparsers.add_parser(
        "show-env",
        help="Display resolved configuration and credential path.",
    )
    return parser


def main() -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "show-env":
        show_env(args.project_id, args.database_id)
        return 0

    if args.command == "seed":
        payload = parse_json_payload(args.data)
        seed_document(
            collection=args.collection,
            document_id=args.document_id,
            payload=payload,
            project_id=args.project_id,
            database_id=args.database_id,
            merge=args.merge,
        )
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
