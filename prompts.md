# Prompts Guardados - Ayuda Memoria

Este archivo resume como quedo configurada tu biblioteca de prompts y como usarla rapido en el dia a dia.

## Lo que ya se configuro

1. Se creo la skill local `prompt-library` en:
   `/Users/emanuel/.codex/skills/prompt-library`
2. Se creo la biblioteca de prompts en:
   `/Users/emanuel/.codex/skills/prompt-library/references/prompts.md`
3. Se agrego la funcion `promptlib` en tu `~/.zshrc` para consultar prompts desde terminal.
4. Se corrigio compatibilidad para que funcione aunque no tengas `rg` instalado (usa `grep` como respaldo).

## Como consultar prompts desde terminal

1. Recargar configuracion de shell (si hace falta):

```bash
source ~/.zshrc
```

2. Ver todos los prompts guardados:

```bash
promptlib
```

3. Ver un prompt puntual por nombre:

```bash
promptlib gitignore-python-github
```

## Donde editar/agregar prompts

Edita directamente este archivo:

`/Users/emanuel/.codex/skills/prompt-library/references/prompts.md`

Formato recomendado para cada entrada:

```md
## nombre-del-prompt
- objetivo: ...
- tags: ...
- ultima_actualizacion: YYYY-MM-DD

### prompt
Texto del prompt.

### variantes (opcional)
- corta: ...
- robusta: ...
```

## Prompt actualmente guardado

- `gitignore-python-github`
- `plantilla-base`

## Tip de uso rapido

Cuando quieras reutilizar uno, puedes pedirme:

- "usa `gitignore-python-github`"
- "guardame este nuevo prompt en la biblioteca"
- "actualiza la variante robusta de X"
