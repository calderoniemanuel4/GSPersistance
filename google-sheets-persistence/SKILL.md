---
name: google-sheets-persistence
description: Persistir, consultar y actualizar datos de agentes en Google Sheets usando Python. Usar cuando se necesite una base ligera y auditable en hojas de cálculo (logs, catálogos, estados de procesos, KV store simple), con autenticación por Service Account, buenas prácticas de código y documentación técnica.
---

# Google Sheets Persistence

## Objetivo

Implementar persistencia de datos en Google Sheets con Python de forma segura y mantenible.
Usar esta skill para crear o mantener integraciones CRUD sobre una hoja, con contrato de datos claro y validación.

## Flujo de trabajo

1. Definir el modelo de datos y elegir una columna clave (`id` por defecto).
2. Configurar credenciales de Google Service Account y compartir la hoja con su email.
3. Inicializar cliente de Sheets con `scripts/google_sheets_store.py`.
4. Asegurar encabezados con `ensure_headers`.
5. Leer/escribir con `get_record`, `upsert_record`, `list_records` y `delete_record`.
6. Registrar errores con logging y manejar excepciones explícitas.
7. Documentar decisiones de esquema y nombres de columnas.

## Estándares obligatorios de Python

- Escribir `type hints` en funciones públicas.
- Agregar docstrings claros (qué hace, parámetros, retorno y errores).
- Validar entradas antes de invocar la API.
- Evitar lógica de negocio dentro de scripts improvisados; reutilizar `GoogleSheetsStore`.
- Usar `logging` en lugar de `print` para trazabilidad.
- Mantener operaciones idempotentes cuando aplique (`upsert` sobre `append` para registros únicos).

## Recursos de la skill

- `scripts/google_sheets_store.py`
  Cliente reutilizable con operaciones CRUD y CLI para pruebas rápidas.
- `references/setup.md`
  Guía de configuración de credenciales, permisos y variables de entorno.

## Uso rápido

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/abs/path/service-account.json"
export GSHEETS_SPREADSHEET_ID="1AbC..."
export GSHEETS_WORKSHEET="state"
python scripts/google_sheets_store.py ensure-headers --headers id,status,updated_at
python scripts/google_sheets_store.py upsert --key job-42 --record '{"status":"done","updated_at":"2026-02-26T10:00:00Z"}'
python scripts/google_sheets_store.py get --key job-42
```

## Criterios de diseño

- Tratar Google Sheets como persistencia ligera, no como OLTP de alta concurrencia.
- Mantener una fila por entidad y una columna clave estable.
- No guardar secretos en celdas.
- Versionar cambios de esquema y migraciones de encabezados.
- Si una operación requiere atomicidad estricta, considerar otro backend y usar Sheets solo como vista/auditoría.

## Instrucción de copia de la skill

- Generar una copia de esta skill y guardarla en una carpeta de `skills` dentro del directorio raíz; si no existe la carpeta, crearla.
