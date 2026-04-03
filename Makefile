MAKEFLAGS += --always-make

VERSION := $(shell python3 rxpw_backend/setup.py --version)

all: build reinstall test


release: all
	if [ -n "${VERSION}" ]; then \
		git tag -a v${VERSION} -m "release v${VERSION}"; \
		git push origin --tags; \
	fi

version:
	@echo ${VERSION}


clean-cover:
	rm -rf cover .coverage coverage.xml htmlcov
clean-tox:
	rm -rf .stestr .tox
clean: build-clean test-clean clean-cover clean-tox


upload:
	python3 -m pip install --upgrade xpip-upload
	xpip-upload --config-file .pypirc rxpw_*/dist/*


build-prepare:
	python3 -m pip install --upgrade -r rxpw_backend/requirements.txt
	python3 -m pip install --upgrade -r rxpw_frontend/requirements.txt
	python3 -m pip install --upgrade xpip-build
build-clean:
	xpip-build --debug --path rxpw_backend setup --clean
	xpip-build --debug --path rxpw_frontend setup --clean
build: build-prepare build-clean
	xpip-build --debug --path rxpw_backend setup --all
	xpip-build --debug --path rxpw_frontend setup --all


install:
	python3 -m pip install --force-reinstall --no-deps rxpw_*/dist/*.whl
uninstall:
	python3 -m pip uninstall -y reflex-xpw-backend
	python3 -m pip uninstall -y reflex-xpw-frontend
reinstall: uninstall install


test-prepare: build-prepare
	python3 -m pip install --upgrade mock pylint flake8 pytest pytest-cov -r requirements-test.txt
pylint:
	pylint $(shell git ls-files rxpw_*/reflex_xpw_*.py)
flake8:
	flake8 rxpw_* --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 rxpw_* --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
pytest:
	pytest --cov=rxpw_backend --cov=rxpw_frontend --cov-report=term-missing --cov-report=xml --cov-report=html --cov-config=.coveragerc --cov-fail-under=100
pytest-clean:
	rm -rf .pytest_cache .states .web
test: test-prepare pylint flake8 pytest
test-clean: pytest-clean
