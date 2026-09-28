.PHONY: install download-data run clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

download-data:
	$(PYTHON) src/download_data.py

run:
	$(PYTHON) src/main.py

clean:
	rm -rf $(VENV) __pycache__ data/raw/* data/processed/*
