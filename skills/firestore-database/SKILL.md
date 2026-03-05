---
name: firestore-database
description: Crear, configurar y poblar una base de datos en Google Cloud Firestore usando Python o la Firebase Admin SDK. Usar cuando Codex necesite habilitar Firestore en un proyecto, preparar credenciales, definir colecciones/documentos iniciales, sembrar datos base, o dejar una integración lista para persistencia en Firestore.
---

# Firestore Database

## Objetivo

Crear una base de datos funcional en Firestore y dejar una base segura para empezar a persistir datos.
Usar esta skill para preparar credenciales, validar conexión y sembrar colecciones o documentos iniciales.

## Flujo de trabajo

1. Confirmar si el usuario necesita:
   - habilitar Firestore en un proyecto nuevo;
   - crear estructura inicial (colecciones/documentos);
   - o integrar una app ya existente.
2. Verificar credenciales de Google Cloud o Firebase Admin SDK.
3. Definir `project_id`, `database_id` y la colección semilla.
4. Revisar `references/setup.md` para elegir el flujo de consola o CLI.
5. Usar `scripts/firestore_bootstrap.py` para validar conexión y sembrar un documento inicial.
6. Documentar la estructura esperada de colecciones, claves y reglas de acceso pendientes.

## Reglas de implementación

- Tratar Firestore como base orientada a documentos: diseñar por patrones de lectura, no por joins.
- Mantener nombres de colecciones estables y en singular o plural de forma consistente.
- Guardar IDs explícitos para datos base importantes; usar IDs automáticos solo cuando no se referencien externamente.
- No incrustar secretos ni rutas locales en el código de aplicación.
- Si faltan reglas de seguridad, dejarlo señalado antes de considerar la integración "lista".
- Sembrar datos mínimos e idempotentes cuando sea posible.

## Recursos de la skill

- `scripts/firestore_bootstrap.py`
  Script reutilizable para inicializar el cliente y escribir un documento semilla desde JSON.
- `references/setup.md`
  Guía rápida para credenciales, habilitación de Firestore y decisiones de modelado inicial.

## Uso rápido

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/abs/path/service-account.json"
export FIRESTORE_PROJECT_ID="mi-proyecto"
python skills/firestore-database/scripts/firestore_bootstrap.py show-env
python skills/firestore-database/scripts/firestore_bootstrap.py seed \
  --collection app_config \
  --document-id bootstrap \
  --data '{"status":"ready","created_by":"codex"}' \
  --merge
```

## Criterios de salida

- Existe una base de datos Firestore habilitada o una instrucción concreta para habilitarla.
- Las credenciales mínimas están definidas y verificadas.
- Hay al menos una colección/documento de prueba o semilla.
- La estructura inicial quedó documentada con nombres claros.
