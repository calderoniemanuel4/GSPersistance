# QR Generator CLI

Aplicacion de terminal en Python para generar codigos QR escaneables desde un celular.

## Estructura

```text
qr-generator-cli/
├── main.py
├── requirements.txt
├── .env.example
├── README.md
└── qr generated/
```

## Requisitos

- Python 3.10+

## Instalacion

```bash
cd qr-generator-cli
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

```bash
python main.py
```

La app solicita una direccion de internet por terminal y guarda la imagen QR en `qr generated/`.

## Nota

Si el usuario ingresa una direccion sin `http://` o `https://`, la app agrega `https://` automaticamente.
