# AGENTS.md

## Propósito

Este archivo define el marco de trabajo para Codex y otros agentes que colaboren en los proyectos de Emanuel. Debe servir como referencia persistente entre sesiones para mantener consistencia técnica, estilo de desarrollo, arquitectura y prioridades.

---

## Contexto general del workspace

* Lenguaje principal: **Python**.
* Lenguajes secundarios posibles: **HTML**, y eventualmente JavaScript mínimo si el proyecto lo requiere.
* Enfoque principal: **APIs, automatización, agentes, integraciones y dashboards**.
* Plataformas cloud preferidas: **Google Cloud Run** y **Google Cloud Functions**.
* Hojas de cálculo: **Google Sheets**.
* Base de datos, autenticación y almacenamiento: **Firestore**.
* Interfaz rápida y visual: **Streamlit**.
* Pruebas rápidas y validaciones iniciales: **terminal de comandos**.
* Integraciones frecuentes: **APIs REST, archivos JSON, servicios cloud, OpenAI, Google Cloud**.

---

## Filosofía de trabajo

1. **Priorizar simplicidad y claridad**.
2. **Evitar complejidad innecesaria** y no reinventar la rueda.
3. **Proponer alternativas** cuando exista más de una solución razonable.
4. **Documentar bien** el código y las decisiones.
5. **Mantener contexto entre sesiones**: cada proyecto debe dejar clara su estructura, propósito, dependencias y próximos pasos.
6. **Pensar como ingeniero de software profesional**, pero sin sobrediseñar.
7. **Código limpio, legible y refactorizable**. Evitar spaghetti code.

---

## Expectativas para Codex / Agentes

Cuando Codex trabaje en un proyecto, debe:

* Entender el objetivo antes de empezar a escribir código.
* Proponer una arquitectura breve antes de implementar si el proyecto tiene mas de un modulo, varias capas o una decision tecnica no obvia.
* Sugerir opciones si hay varias formas válidas de resolver algo.
* Generar proyectos ordenados, con carpetas y archivos descriptivos.
* Escribir código modular, reutilizable y orientado a objetos cuando tenga sentido.
* Incluir **docstrings claros** en clases, funciones y módulos.
* Seguir buenas prácticas de tipado, validación y manejo de errores.
* Favorecer herramientas modernas y mantenibles.
* Explicar brevemente decisiones importantes de diseño.

### Regla de proporcionalidad

La solucion debe ser proporcional al problema.

* Si la tarea es pequena, preferir una implementacion simple, directa y facil de mantener.
* Si es un prototipo o prueba rapida, evitar sobredisenar la estructura.
* Si el proyecto va a crecer, modularizar desde temprano.
* No forzar capas, clases o carpetas si no aportan claridad real.

---

## Stack preferido

### Python

Priorizar:

* `pydantic` para validación de datos y modelos.
* `fastapi` para APIs.
* `httpx` para llamadas HTTP.
* `pytest` para tests.
* `python-dotenv` para variables de entorno locales.
* `google-cloud-firestore` para Firestore.
* `gspread` y `google-auth` para Google Sheets cuando aplique.
* `streamlit` para interfaces rápidas.
* `uvicorn` para correr APIs locales.
* `rich` o `typer` para CLIs agradables cuando sea útil.

### Cloud / Infraestructura

* Despliegues en **Google Cloud Run** o **Google Cloud Functions** según el caso.
* Firestore como base de datos principal.
* Google Sheets como apoyo operativo, reporting o prototipos rápidos.
* Uso de variables de entorno y secretos en vez de credenciales hardcodeadas.

---

## Convenciones de arquitectura

### Regla general

Cada proyecto debe arrancar con una estructura ordenada. Como base, preferir algo similar a:

```text
project_name/
├── app/
│   ├── api/
│   ├── services/
│   ├── models/
│   ├── core/
│   └── utils/
├── tests/
├── scripts/
├── docs/
├── .env.example
├── requirements.txt
├── README.md
└── main.py
```

Estas estructuras son guias para proyectos medianos o con vocacion de crecer. En proyectos pequenos, se puede usar una version mas simple mientras el codigo siga siendo claro.

### Si el proyecto usa FastAPI

Preferir:

```text
project_name/
├── app/
│   ├── api/
│   │   └── routes/
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   └── main.py
├── tests/
├── scripts/
├── requirements.txt
├── README.md
└── .env.example
```

### Si el proyecto usa Streamlit

Preferir:

```text
project_name/
├── app/
│   ├── pages/
│   ├── components/
│   ├── services/
│   ├── models/
│   └── streamlit_app.py
├── tests/
├── scripts/
├── data/
├── requirements.txt
├── README.md
└── .env.example
```

### Estructura minima permitida

Si el proyecto es pequeno o exploratorio, esta estructura tambien es valida:

```text
project_name/
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .env.example
```

---

## Estilo de código

* Usar nombres de archivos, clases y funciones descriptivos.
* Mantener funciones pequeñas y enfocadas.
* No mezclar lógica de negocio con lógica de presentación.
* Evitar archivos gigantes con demasiadas responsabilidades.
* Usar clases cuando aporten organización real.
* Usar tipado estático en funciones y métodos.
* Centralizar configuración en un módulo de settings.
* Separar claramente:

  * modelos
  * servicios
  * repositorios
  * rutas
  * utilidades

---

## Docstrings y documentación

Todo módulo importante debe incluir:

* propósito del archivo
* cómo se usa
* dependencias relevantes

Toda clase o función pública debe incluir docstring. Preferir estilo claro tipo:

```python
def load_messages(sheet_id: str) -> list[dict]:
    """Load messages from a Google Sheet.

    Args:
        sheet_id: Google Sheet identifier.

    Returns:
        A list of message dictionaries.
    """
```

Además:

* cada proyecto debe tener un `README.md`
* incluir pasos de instalación
* variables de entorno requeridas
* comandos de ejecución local
* comandos de deploy si aplica

---

## Manejo de configuración

* Nunca hardcodear claves o secretos.
* Usar `.env` para desarrollo local.
* Generar siempre `.env.example`.
* Preferir clases de configuración con `pydantic` o configuración centralizada.

---

## Calidad y testing

* Incluir tests básicos en todo proyecto que crezca más allá de una prueba rápida.
* Cubrir al menos:

  * parsing de datos
  * servicios principales
  * validaciones
  * rutas críticas si hay API
* Si no se escriben tests completos, dejar al menos una sección `TODO` con recomendaciones claras.
* Para utilidades pequenas o demos, al menos validar ejecucion local y documentar como probarlo manualmente.

---

## Convenciones del workspace

* Usar `requirements.txt` en proyectos pequenos o prototipos. Si el proyecto crece bastante, se puede migrar a `pyproject.toml`.
* Preferir `pytest` como framework de testing por defecto.
* Agregar `.gitignore` en la raiz del workspace o del proyecto segun corresponda.
* Nunca versionar secretos, credenciales, archivos `.env`, certificados o claves privadas.
* Incluir `README.md` con instalacion, ejecucion y notas operativas minimas.
* Incluir `.env.example` cuando el proyecto use configuracion por variables de entorno.
* Si hay varias miniapps dentro del mismo workspace, cada una debe vivir en su propia carpeta con sus archivos principales.
* Evitar mezclar codigo experimental con codigo estable sin separarlo por carpetas o documentarlo.

### Archivos que normalmente no deben subirse

* `__pycache__/`
* `.pytest_cache/`
* `.mypy_cache/`
* `.ruff_cache/`
* `.venv/`
* `.env`
* `.env.*`
* `*.pem`
* `*.key`
* `credentials*.json`
* `.DS_Store`

### Comandos preferidos

* Ejecutar tests con `pytest`.
* Validar scripts simples con la terminal antes de proponer despliegue.
* Ejecutar apps Streamlit con `streamlit run ...` o `python -m streamlit run ...`.

---

## Integraciones y persistencia

### Firestore

Usar Firestore como opción principal para:

* persistencia estructurada
* configuración por usuario
* logs de ejecución
* historiales
* autenticación y datos de app

### Google Sheets

Usar Google Sheets para:

* reporting
* dashboards rápidos
* análisis operativo
* prototipos
* exportaciones o logs visibles para negocio

### JSON

Usar archivos JSON para:

* mocks
* configuración temporal
* intercambio de datos simple
* snapshots de pruebas

---

## Interfaces

### Terminal

Primera opción para validar rápido:

* scripts ejecutables
* CLIs simples
* pruebas de flujo
* debugging inicial

### Streamlit

Usar para:

* dashboards
* paneles operativos
* interfaces de prueba
* visualización rápida de datos

### HTML

Solo incorporarlo cuando haya una necesidad clara de UI web más personalizada.

---

## Despliegue

Antes de preparar deploy, Codex debe:

1. verificar estructura del proyecto
2. revisar dependencias
3. validar variables de entorno necesarias
4. proponer estrategia de despliegue adecuada:

   * Cloud Functions para funciones pequeñas, webhooks o automatizaciones puntuales
   * Cloud Run para APIs o servicios más completos

---

## Forma de respuesta esperada de Codex

Cuando trabaje sobre un proyecto, preferir este formato:

1. **Resumen breve del objetivo**
2. **Propuesta de estructura o enfoque** si hace falta
3. **Implementación**
4. **Cómo correrlo**
5. **Siguientes mejoras opcionales**

Si hay más de una alternativa válida, mostrar:

* opción simple
* opción robusta

---

## Regla final

Construir como si el proyecto pudiera crecer:

* ordenado desde el día 1
* fácil de entender en una semana
* fácil de refactorizar en un mes
* fácil de desplegar en producción si madura

Este workspace prioriza proyectos bien pensados, modulares, claros y profesionales.

Sin embargo, claridad no significa complejidad. Si una solucion pequena resuelve bien el problema, esa debe ser la opcion preferida.
