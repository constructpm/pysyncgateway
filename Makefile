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

.PHONY: dev
dev:
	$(bin_prefix)pip install -r requirements/dev.txt

.PHONY: requirements
requirements:
	$(bin_prefix)pip-compile requirements.in

.PHONY: lint
lint:
	@echo "=== flake8 ==="
	$(bin_prefix)flake8 pysyncgateway tests
	@echo "=== isort ==="
	$(bin_prefix)isort --quiet --recursive --diff pysyncgateway tests > isort.out
	if [ "$$(wc -l isort.out)" != "0 isort.out" ]; then cat isort.out; exit 1; fi
	@echo "=== yapf ==="
	$(bin_prefix)yapf --recursive --diff pysyncgateway tests

.PHONY: test
test:
	$(bin_prefix)pytest

.PHONY: doc
doc:
	$(bin_prefix)sphinx-apidoc -f -o docs pysyncgateway/
	$(MAKE) -C docs html
