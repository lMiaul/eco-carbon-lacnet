# Eco-Carbon San Martín — ZIP Maestro

Este paquete contiene:
- **CORE** (en la raíz): listo para ejecutar por CLI y correr tests.
- **EXTRAS** (en `/extras`): interfaz Jupyter (ipywidgets), CI y requisitos extra.

## Uso rápido (CORE)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.ecocarbon.cli --demo --pilot 5 --no-ui
pytest -q
```

## Activar EXTRAS
Copia el contenido de `/extras` sobre la raíz del proyecto si deseas UI/CI:
```bash
cp -r extras/* ./
# Instala extras si los necesitas
pip install -r extras/requirements.txt  # o integra las dependencias al requirements principal
```
