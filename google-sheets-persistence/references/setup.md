# Setup Google Sheets como persistencia

## 1. Crear Service Account

1. Entrar a Google Cloud Console y crear/probar un proyecto.
2. Habilitar la API de Google Sheets.
3. Crear una Service Account.
4. Generar una clave JSON y guardarla en una ruta segura local.

## 2. Compartir la hoja

1. Abrir el Google Sheet destino.
2. Compartirlo con el correo de la Service Account (permiso Editor).
3. Copiar el `spreadsheet_id` desde la URL.

## 3. Variables de entorno

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/abs/path/service-account.json"
export GSHEETS_SPREADSHEET_ID="1AbCdEf..."
export GSHEETS_WORKSHEET="state"
export GSHEETS_KEY_COLUMN="id"
```

## 4. Dependencias Python

```bash
pip install gspread google-auth
```

## 5. Smoke test

```bash
python scripts/google_sheets_store.py ensure-headers --headers id,status,updated_at
python scripts/google_sheets_store.py upsert --key test-1 --record '{"status":"ok","updated_at":"2026-02-26T00:00:00Z"}'
python scripts/google_sheets_store.py get --key test-1
```

## 6. Recomendaciones de diseño

- Mantener encabezados estables y en `snake_case`.
- Usar timestamps ISO-8601 UTC.
- Evitar estructuras anidadas; serializar JSON cuando sea necesario.
- No guardar secretos ni PII sensible sin controles adicionales.
