venv_folder=venv

# If venv_folder does not exist and we're not running tox
ifneq "$(wildcard $(venv_folder) )" ""
ifneq "$(IN_TOX)" "1"
bin_prefix=$(venv_folder)/bin/
endif
endif

lint_files=pysyncgateway tests setup.py
rst_files=README.rst CHANGELOG.rst

.PHONY: venv
venv:
	virtualenv $(venv_folder)
	$(venv_folder)/bin/pip install -U pip

# Used by Circle to get tox
.PHONY: install
install:
	$(bin_prefix)pip install tox

.PHONY: pip-tools
pip-tools:
	$(bin_prefix)pip install pip-tools

# Install dev environment
.PHONY: dev
dev: pip-tools
	$(bin_prefix)pip-sync requirements/dev.txt

# --- TESTING ---

.PHONY: flake8
flake8:
	@echo "=== flake8 ==="
	$(bin_prefix)flake8 pysyncgateway $(lint_files)

.PHONY: lint
lint: flake8
	@echo "=== isort ==="
	$(bin_prefix)isort --quiet --recursive --diff $(lint_files) > isort.out
	if [ "$$(wc -l isort.out)" != "0 isort.out" ]; then cat isort.out; exit 1; fi
	@echo "=== yapf ==="
	$(bin_prefix)yapf --recursive --diff $(lint_files)
	@echo "=== rst ==="
	$(bin_prefix)restructuredtext-lint $(rst_files)

.PHONY: tox
tox:
	$(bin_prefix)tox

.PHONY: fixlint
fixlint: flake8
	@echo "=== fixing isort ==="
	$(bin_prefix)isort --recursive $(lint_files)
	@echo "=== fixing yapf ==="
	$(bin_prefix)yapf --recursive --in-place $(lint_files)

.PHONY: doc
doc:
	$(bin_prefix)sphinx-apidoc -f -o docs pysyncgateway/
	$(MAKE) -C docs doctest html


# --- Building / Publishing ---

.PHONY: clean
clean:
	rm -rf dist build .tox
	find . -name '*.pyc' -delete
	$(MAKE) -C docs clean

.PHONY: sdist
sdist: clean tox
	$(bin_prefix)python setup.py sdist

.PHONY: bdist_wheel
bdist_wheel: clean tox
	$(bin_prefix)python setup.py bdist_wheel

.PHONY: testpypi
testpypi: clean sdist bdist_wheel
	$(bin_prefix)twine upload --repository-url https://test.pypi.org/legacy/ dist/*
