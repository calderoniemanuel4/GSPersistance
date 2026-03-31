## TODO
    -Implementar esta app en una pagina web y subirla a cloud run.
    -MCP firebase por ahora. Se le debe dar permisos para usar el servicio
    -pedir a Codex bajar un repo de una app o scrip , analizarlo, mejorarlo e instalarlo local.

## Anotaciones Codex
    -Conectamos el workspace con nuestro repo en github:
        *git add .
        *git commit
        *git push origin master
    -vamos a trabajar con streamlit (MVP) similar tkinter que recomendo ChatGPT
    -bash: streamlit run streamlit_app.py
    -VSCode como editor 
    -CODEX lleva control de diff + - sobre todo el proyecto. Cuyando Hacemos commit las diff desaparecen. Podemos hacer commit and push desde el panel superior. Desde la vista diff se puede abrir el arbol de archivos.
    -THREADS:
         son ramas en donde podemos lanzar una tarea sobre un environment o proyecto comun. Es decir podemos lanzar  multiagentes en paralelo que trabajan en un environment(se debe seleccionar el proyecto). Ejemplo: Agente diseño, agente seguridad, agente autenticacion, agente base de datos, etc.
    -creamos un AGENTS.MD  generado por IA para q CODEX recuerde la forma de desarrollar nuestros proyectos entre sesiones 
    -Vimos un prompt donde se pide crear un simple HTML para volcar los resultados del proyecto, que tenga buen diseño y explique los conceptos. Posteriormente en otro prompt se agrego botones(Descargar resultados, ver mas ejemplos, ver en google sheets)
    -AUTOMATIONS:
        #Implementa tareas programadas.
        #Puede ser ejecutar una automatizacion disponible o crear una nueva.
        #Para crear una nueva debe escribirse un prompt. Puede incluir skills.
        # Cada vez que se ejecuta una automatizacion abre un hilo/thread donde queda el historial de la ejecucion.
        #Ejemplos: Tareas de limpieza en el entorno, actualizar AGENTS.md, ejecutar un script.
    -CONTEXTO:
        AGENTS.md en la raíz: reglas globales del proyecto.
        README.md por cada app/módulo: qué hace, cómo correrlo y límites.
        docs/decisions.md o ARCHITECTURE.md: decisiones clave (por qué se hizo así).
        tasks/ con tickets en markdown: objetivo, alcance, criterios de aceptación.
    -LENGUAJES:
        Nuestros lenguajes seran: Python, bash, Json y en menor medida HTML,  Markdown.


## Proyectos y avances 
    -Se implemento una app que convierte pies a metros: Nice!😎
    -instalamos un MCP con contex7 , esto se incorporo en agents.md para que los proyectos consulten la documentacion de las APIs y librerias que se utilicen. 

## Como conversar con Codex
    Aquí tienes una mini chuleta práctica para usar conmigo en Codex:

    -Revisa @conversor de pies/streamlit_app.py y explícame qué hace.
    -Edita @conversor de pies/streamlit_app.py para validar números negativos y cero.
    -Crea un README.md para @conversor de pies con instalación y uso.
    -Compara @AGENTS.md con @conversor de pies/README.md y dime qué falta.
    -Usa skill-creator para crear una skill que genere apps Streamlit base.
    -Usa skill-installer para instalar una skill desde un repo de GitHub.
    -Revisa este bloque y mejóralo sin cambiar el comportamiento:
        def convert_value(value: float, unit: str) -> tuple[float, str]:
            if unit == "Pies":
                return value * 0.3048, "metros"
            return value / 0.3048, "pies"
    -Busca en este proyecto dónde se usa convert_value.
    -Agrega tests para @conversor de pies/streamlit_app.py.
    -Dime exactamente qué comandos debo correr para ejecutar este proyecto        localmente.
