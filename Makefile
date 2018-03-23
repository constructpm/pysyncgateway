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
	$(bin_prefix)pip install -r requirements/test.txt

.PHONY: pip-tools
pip-tools:
	$(bin_prefix)pip install pip-tools

.PHONY: dev
dev: pip-tools
	$(bin_prefix)pip-sync requirements/dev.txt

.PHONY: requirements
requirements: pip-tools
	$(bin_prefix)pip-compile requirements.in

.PHONY: flake8
flake8:
	@echo "=== flake8 ==="
	$(bin_prefix)flake8 pysyncgateway tests setup.py

.PHONY: lint
lint: flake8
	@echo "=== isort ==="
	$(bin_prefix)isort --quiet --recursive --diff pysyncgateway tests > isort.out
	if [ "$$(wc -l isort.out)" != "0 isort.out" ]; then cat isort.out; exit 1; fi
	@echo "=== yapf ==="
	$(bin_prefix)yapf --recursive --diff pysyncgateway tests

.PHONY: fixlint
fixlint: flake8
	@echo "=== fixing isort ==="
	$(bin_prefix)isort --recursive pysyncgateway tests
	@echo "=== fixing yapf ==="
	$(bin_prefix)yapf --recursive --in-place pysyncgateway tests

.PHONY: test
test:
	$(bin_prefix)pytest

.PHONY: doc
doc:
	$(bin_prefix)sphinx-apidoc -f -o docs pysyncgateway/
	$(MAKE) -C docs html
