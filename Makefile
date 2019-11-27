upload:
	rm -rf dist/*
	python3 setup.py sdist
	# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	# twine upload --repository-url https://testpypi.python.org/pypi dist/*
	twine upload --repository testpypi dist/*
	

cleanc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*.so' -exec rm -f {} +
	find . -name '*.c' -exec rm -f {} +

buildc: cleanc
	python3 setup.py build_ext --inplace -if

cupload: buildc upload

