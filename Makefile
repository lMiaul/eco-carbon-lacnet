.PHONY: install test demo ui clean

VENV := .venv
PY := python
PIP := $(VENV)/bin/pip

$(VENV)/bin/activate:
	$(PY) -m venv $(VENV)
	$(PIP) install --upgrade pip

install: $(VENV)/bin/activate
	$(PIP) install -r requirements.txt

test: install
	$(VENV)/bin/pytest -q

demo: install
	$(VENV)/bin/python -m src.ecocarbon.cli --demo --pilot 5 --no-ui

ui:
	@echo "Abrir Jupyter y ejecutar:"
	@echo "from src.ecocarbon.interface import EcoCarbonInterface"
	@echo "EcoCarbonInterface().create_widgets()"

clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache htmlcov .coverage
