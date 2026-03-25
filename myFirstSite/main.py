"""Abrir la página local de buenas prácticas de Python en el navegador.

Uso:
    python3 main.py
"""

from pathlib import Path
import webbrowser


def open_local_page() -> None:
    """Open the local HTML page in the default browser."""
    base_dir = Path(__file__).resolve().parent
    html_path = base_dir / "python_buenas_practicas.html"

    if not html_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo HTML: {html_path}")

    webbrowser.open_new_tab(html_path.as_uri())


if __name__ == "__main__":
    open_local_page()
