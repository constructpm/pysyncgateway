venv_folder=venv

# If venv_folder does not exist:
ifneq "$(wildcard $(venv_folder) )" ""
    bin_prefix=$(venv_folder)/bin/
endif

.PHONY: venv
venv:
	virtualenv $(venv_folder)
	$(venv_folder)/bin/pip install -U pip

.PHONY: install
install:
	$(bin_prefix)pip install -r requirements/base.txt

.PHONY: dev
dev:
	$(bin_prefix)pip install -r requirements/dev.txt

.PHONY: requirements
requirements:
	$(bin_prefix)pip-compile requirements.in

.PHONY: test
test:
	$(bin_prefix)pytest
