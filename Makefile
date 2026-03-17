.SILENT:
.PHONY: install run debug clean lint lint-strict
.SILENT:

VENV := a-maze-ing-venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
FLAKE8 := python3 -m flake8 .
MYPY := python3 -m mypy .
MAIN := a_maze_ing.py

install:
	@echo "Creation of the venv if necessary..."
	test -d a-maze-ing-venv || python3 -m venv a-maze-ing-venv
	@echo "Activation of the venv and installation of dependancies..."
	a-maze-ing-venv/bin/activate
	$(PIP) install mlx_downloader/mlx-2.2-py3-none-any.whl
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pytest flake8 mypy

run:
	$(PYTHON) $(MAIN)

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	rm -rf $(VENV)
	rm -rf __pycache__ .mypy_cache .pytest_cache Utils/__pycache__ .vscode

lint:
	$(FLAKE8) .
	$(MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(FLAKE8) .
	$(MYPY) . --strict

test:
	PYTHONPATH=$(PWD) $(PYTEST) tests