.PHONY: install run debug clean lint lint-strict

PYTHON := /tmp/a-maze-ing-venv/bin/python3
PIP := /tmp/a-maze-ing-venv/bin/pip
PYTEST := /tmp/a-maze-ing-venv/bin/pytest
FLAKE8 := /tmp/a-maze-ing-venv/bin/flake8
MYPY := /tmp/a-maze-ing-venv/bin/mypy

MAIN := a_maze_ing.py

install:
	@echo "Creation of the venv if necessary..."
	test -d /tmp/a-maze-ing-venv || python3 -m venv /tmp/a-maze-ing-venv
	@echo "Activation of the venv and installation of dependancies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pytest flake8 mypy

run:
	$(PYTHON) $(MAIN)

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
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