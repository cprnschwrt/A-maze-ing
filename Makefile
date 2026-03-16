.PHONY: install run debug clean lint lint-strict
.SILENT:
PYTHON := /tmp/a-maze-ing-venv/bin/python3
PIP := /tmp/a-maze-ing-venv/bin/pip
PYTEST := /tmp/a-maze-ing-venv/bin/pytest
FLAKE8 := python3 -m flake8 .
MYPY := python3 -m mypy .

VE := a-maze-ing
MAIN := a_maze_ing.py

install:
	@echo "Creation of the venv if necessary..."
	test -d /tmp/a-maze-ing-venv || python3 -m venv /tmp/a-maze-ing-venv
	@echo "Activation of the venv and installation of dependancies..."
	pip install mlx_downloader/mlx-2.2-py3-none-any.whl
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pytest flake8 mypy

run:
	python3 $(MAIN)

venv:
	python -m venv $(VE);

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	rm -rf $(VE)
	rm -rf __pycache__ .mypy_cache .pytest_cache
	rm -rf /tmp/a-maze-ing-venv

lint:
	$(FLAKE8) .
	$(MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(FLAKE8) .
	$(MYPY) . --strict

test:
	PYTHONPATH=$(PWD) $(PYTEST) tests