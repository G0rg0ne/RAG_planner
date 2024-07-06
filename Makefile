help:
	@cat Makefile

.EXPORT_ALL_VARIABLES:

# create an .env file to override the default settings
-include .env
export $(shell sed 's/=.*//' .env)

# Variables
PYTHON_EXEC?=python -m
EXAMPLE_DIR:=./examples

# Installation
install-init:
	$(PYTHON_EXEC) pip install --upgrade pip
	$(PYTHON_EXEC) pip install --upgrade poetry
	$(PYTHON_EXEC) poetry self update

install: install-init
	$(PYTHON_EXEC) poetry install --no-cache