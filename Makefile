
# clean all the temp files for clean build
cleanc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*.so' -exec rm -f {} +
	find . -name '*.c' -exec rm -f {} +
	rm -rf .eggs
	rm -rf .pytest_cache
	rm -rf .tox

# build so and .c files
buildc: cleanc
	python3 setup.py build_ext --inplace -if


# test using tox
test: buildc
	tox

# fast test without removing caches
fasttest: 
	python3 setup.py build_ext --inplace -if
	tox

# upload to pypi
pypiupload: test
	rm -rf dist/*
	python3 setup.py sdist
	twine upload dist/*

# upload to test pypi repo
testpypiupload: test
	rm -rf dist/*
	python3 setup.py sdist
	twine upload --repository testpypi dist/*
	

