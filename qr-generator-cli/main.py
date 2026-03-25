"""CLI app to generate scannable QR codes from URLs.

Usage:
    python main.py
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import qrcode

OUTPUT_DIR = Path(__file__).resolve().parent / "qr generated"


def normalize_url(raw_url: str) -> str:
    """Normalize user input into a valid URL string.

    Args:
        raw_url: URL entered by the user.

    Returns:
        A normalized URL string.

    Raises:
        ValueError: If URL is empty or invalid.
    """
    cleaned = raw_url.strip()
    if not cleaned:
        raise ValueError("La direccion no puede estar vacia.")

    if not cleaned.startswith(("http://", "https://")):
        cleaned = f"https://{cleaned}"

    parsed = urlparse(cleaned)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("La direccion ingresada no parece valida.")

    return cleaned


def build_output_path() -> Path:
    """Build a timestamped output path for the QR image."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return OUTPUT_DIR / f"qr_{timestamp}.png"


def generate_qr(url: str, output_path: Path) -> None:
    """Generate and save a QR image for a given URL.

    Args:
        url: URL to encode.
        output_path: Final output image path.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=12,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    image.save(output_path)


def main() -> None:
    """Run the command-line flow to generate a QR code image."""
    print("Generador de QR")
    raw_url = input("Ingresa una direccion de internet: ")

    try:
        normalized_url = normalize_url(raw_url)
    except ValueError as error:
        print(f"Error: {error}")
        return

    output_path = build_output_path()
    generate_qr(normalized_url, output_path)

    print("QR generado correctamente.")
    print(f"URL codificada: {normalized_url}")
    print(f"Archivo: {output_path}")


if __name__ == "__main__":
    main()
