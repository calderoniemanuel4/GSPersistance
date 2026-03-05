# Setup de Firestore

## Qué significa "crear la base de datos"

En Firestore, primero se habilita una base de datos para el proyecto.
Después, las colecciones y documentos se crean de forma implícita cuando escribes el primer dato.

## Preparación mínima

1. Confirmar el `project_id`.
2. Habilitar Firestore en el proyecto desde Firebase Console o Google Cloud Console.
3. Elegir modo nativo de Firestore (el habitual para apps nuevas).
4. Crear o descargar una Service Account con permisos para leer y escribir en Firestore.
5. Exportar `GOOGLE_APPLICATION_CREDENTIALS` con la ruta absoluta del JSON.

## Variables útiles

- `GOOGLE_APPLICATION_CREDENTIALS`: ruta al JSON de la service account.
- `FIRESTORE_PROJECT_ID`: ID del proyecto.
- `FIRESTORE_DATABASE_ID`: opcional; usa `(default)` si no se especifica otra base.

## Modelado inicial recomendado

- Crear primero una colección pequeña y estable, por ejemplo `app_config`, `tenants` o `users`.
- Guardar un documento semilla con metadata básica (`status`, `created_at`, `created_by`).
- Definir desde el inicio qué campo funciona como referencia externa (`slug`, `email`, `external_id`).
- Evitar arrays crecientes sin límite dentro del mismo documento.

## Validación mínima

- Leer el documento recién escrito.
- Confirmar que el entorno apunta al proyecto correcto.
- Anotar si faltan reglas de seguridad, índices compuestos o emulador local.
