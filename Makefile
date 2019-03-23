.PHONY: compile annotate patch minor major release clean


PROJECT_DIR=elasticsearch_partition

PYTHON ?= python


compile:
	$(PYTHON) setup.py build_ext --inplace


annotate:
	cython $(PROJECT_DIR)/*.pyx -a


patch:
	bumpversion patch


minor:
	bumpversion minor


major:
	bumpversion major


release: clean
	$(PYTHON) setup.py sdist bdist_wheel
	twine upload dist/*


clean:
	rm -rf dist/
	rm -rf build/
	rm -rf $(PROJECT_DIR)/__pycache__
	rm -f $(PROJECT_DIR)/*.pyc
	rm -f $(PROJECT_DIR)/*.c
	rm -f $(PROJECT_DIR)/*.so
	rm -f $(PROJECT_DIR)/*.html
