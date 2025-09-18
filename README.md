# Eco-Carbon San Martín (Preliminary Python)

**Estado:** Implementación preliminar en Python para pruebas mientras se habilita el despliegue en **LAC-Net**.
Simula: residuos → biochar → tCO₂eq → tokens **ECOCO2**, con **CLI** y **UI para Jupyter** incluidas en este repositorio.

## Requisitos
- Python 3.10+

## Instalación
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Estructura
```
src/
  ecocarbon/
    __init__.py
    contract.py
    simulator.py
    interface.py
    cli.py
tests/
.github/workflows/ci.yml
```

## Uso (CLI, sin interfaz)
```bash
python -m src.ecocarbon.cli --demo --pilot 10 --no-ui
```
- `--demo`: corre la demostración inicial (acuña un lote, balance, distribución).
- `--pilot N`: simula N lotes de piloto y muestra sumario.
- `--no-ui`: evita intentar cargar la interfaz (útil fuera de Jupyter).

## Uso (UI en Jupyter/Colab)
En una celda de notebook:
```python
from src.ecocarbon.interface import EcoCarbonInterface
ui = EcoCarbonInterface()
ui.create_widgets()
```

## Tests
```bash
pytest -q
```

## Notas clave
- Conversión CO₂ alineada: **11.04 tCO₂eq / tonelada de biochar** ⇒ `0.01104` tCO₂eq por kg.
- Rol `RETIREMENT` concedido al admin por defecto para permitir retiros en las demos.
- Eliminada instalación de paquetes en runtime; usa `requirements.txt`.

## Uso con Makefile (Unix/macOS/Linux)
Comandos rápidos:
```bash
make install   # crea venv y instala dependencias (versiones fijadas)
make test      # ejecuta pytest -q
make demo      # corre demo CLI (5 lotes) sin UI
```

> En Windows, usa los comandos manuales del bloque de Instalación/CLI,
> o ejecuta `make` si tienes Make instalado (por ejemplo con Git Bash).

## Versiones fijadas (reproducibilidad)
Este repo fija versiones en `requirements.txt`:
```
numpy==1.26.* 
pandas==2.2.* 
matplotlib==3.8.* 
ipywidgets==8.1.* 
folium==0.16.* 
geopy==2.4.* 
pytest==8.3.*
```
Así evitamos cambios de API por actualizaciones mayores. Si necesitas actualizarlas,
ajusta el archivo y valida con `make test`.

## Licencia
MIT (ver `LICENSE`).
