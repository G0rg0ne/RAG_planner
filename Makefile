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
	# Upgrade pip and install Poetry (if not already installed)
	$(PYTHON_EXEC) pip install --upgrade pip
	$(PYTHON_EXEC) pip install --upgrade poetry
	# Ensure Poetry is using the latest version if needed
	$(PYTHON_EXEC) poetry self update

install: install-init
	# Install project dependencies using Poetry
	$(PYTHON_EXEC) poetry install --no-cache