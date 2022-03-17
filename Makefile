### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

PACKAGE_NAME=kitconcept.api
PACKAGE_PATH=src/kitconcept/api
CHECK_PATH=setup.py $(PACKAGE_PATH)


# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr bin include lib lib64 pyvenv.cfg .python-version
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/

.PHONY: install-dev-tools
install-dev-tools: bin/pip ## Install dev-tools
	@echo "$(GREEN)==> Install dev tools$(RESET)"
	bin/pip install -r requirements/dev-tools.txt

bin/pip:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	python -m venv .
	bin/pip install -U pip
	bin/pip install -U setuptools

bin/black:
	@make install-dev-tools

bin/flakeheaven:
	@make install-dev-tools

bin/isort:
	@make install-dev-tools

bin/zpretty:
	@make install-dev-tools

bin/mkwsgiinstance:	bin/pip
	@echo "$(GREEN)==> Install Plone and create instance$(RESET)"
	bin/pip install -r requirements/plone.txt
	bin/mkwsgiinstance -d . -u admin:admin

.PHONY: build
build: bin/mkwsgiinstance ## Install Plone 6 and install the package
	@echo "$(GREEN)==> Install Plone 6, create instance and install the package$(RESET)"
	bin/pip install -r requirements.txt

.PHONY: build-dev
build-dev: bin/mkwsgiinstance ## Install Plone 6 and install the package (with development packages)
	@echo "$(GREEN)==> Install Plone 6, create instance and install the package$(RESET)"
	bin/pip install -r requirements/dev.txt

.PHONY: build-dev-5
build-dev-5: bin/pip ## Install Plone 5.2 and install the package (with development packages)
	@echo "$(GREEN)==> Install Plone 5.2, create instance and install the package$(RESET)"
	bin/pip install -r requirements/plone5.txt
	bin/mkwsgiinstance -d . -u admin:admin
	bin/pip install -r requirements/dev.txt

.PHONY: black
black: bin/black ## Format codebase
	./bin/black $(CHECK_PATH)

.PHONY: isort
isort: bin/isort ## Format imports in the codebase
	./bin/isort $(CHECK_PATH)

.PHONY: zpretty
zpretty: bin/zpretty ## Format ZCML and ZML code
	find $(CHECK_PATH) -name *.zcml | xargs -r ./bin/zpretty -i -z
	find $(CHECK_PATH) -name *.xml | xargs -r ./bin/zpretty -i -x

.PHONY: format
format: black isort zpretty ## Format the codebase according to our standards

.PHONY: lint
lint: lint-isort lint-black lint-flake8 lint-zpretty ## check style with flake8

.PHONY: lint-black
lint-black: bin/black ## validate black formating
	./bin/black --check --diff $(CHECK_PATH)

.PHONY: lint-flake8
lint-flake8: bin/flakeheaven ## validate flake8 formating
	./bin/flakeheaven lint $(CHECK_PATH)

.PHONY: lint-isort
lint-isort: bin/isort ## validate using isort
	./bin/isort --check-only $(CHECK_PATH)

.PHONY: lint-zpretty
lint-zpretty: bin/zpretty ## validate using zpretty
	find $(CHECK_PATH) -name *.zcml | xargs -r ./bin/zpretty -i -z --check
	find $(CHECK_PATH) -name *.xml | xargs -r ./bin/zpretty -i -x --check

.PHONY: test
test: ## run tests
	./bin/zope-testrunner --auto-color --auto-progress --test-path src/

.PHONY: test_quiet
test_quiet: ## run tests removing deprecation warnings
	PYTHONWARNINGS=ignore ./bin/zope-testrunner --auto-color --auto-progress --test-path src/

.PHONY: start
start: ## Start a Plone instance on localhost:8080
	PYTHONWARNINGS=ignore ./bin/runwsgi etc/zope.ini


# CI
.PHONY: ci-build
ci-build: ## Install package in Github Actions
	@echo "$(GREEN)==> Install package$(RESET)"
	pip install -r requirements/dev.txt

.PHONY: ci-test
ci-test: ## Test package in Github Actions
	@echo "$(GREEN)==> Run tests$(RESET)"
	PYTHONWARNINGS=ignore zope-testrunner --auto-color --auto-progress --test-path src/
