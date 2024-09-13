@echo off

SET 	match=re.match(r'^([a-zA-Z_-]+):.*?

IF /I "%1"==".DEFAULT_GOAL " GOTO .DEFAULT_GOAL 
IF /I "%1"=="try" GOTO try
IF /I "%1"=="except" GOTO except
IF /I "%1"=="webbrowser.open("file" GOTO webbrowser.open("file
IF /I "%1"=="for line in sys.stdin" GOTO for line in sys.stdin
IF /I "%1"=="BROWSER " GOTO BROWSER 
IF /I "%1"=="help" GOTO help
IF /I "%1"=="clean" GOTO clean
IF /I "%1"=="clean-build" GOTO clean-build
IF /I "%1"=="clean-pyc" GOTO clean-pyc
IF /I "%1"=="clean-test" GOTO clean-test
IF /I "%1"=="lint" GOTO lint
IF /I "%1"=="test" GOTO test
IF /I "%1"=="docs" GOTO docs
IF /I "%1"=="servedocs" GOTO servedocs
IF /I "%1"=="test_release" GOTO test_release
IF /I "%1"=="release" GOTO release
IF /I "%1"=="dist" GOTO dist
IF /I "%1"=="install" GOTO install
GOTO error

:.DEFAULT_GOAL 
	CALL make.bat =
	CALL make.bat help
	GOTO :EOF

:try
	from urllib import pathname2url
	GOTO :EOF

:except
	from urllib.request import pathname2url
	GOTO :EOF

:webbrowser.open("file
	CALL make.bat //"
	CALL make.bat +
	CALL make.bat pathname2url(os.path.abspath(sys.argv[1])))
	GOTO :EOF

:for line in sys.stdin
	match = re.match(r'^([a-zA-Z_-]+):.*?
	if match:
	target, help = match.groups()
	print("%-20s %s" % (target, help))
	GOTO :EOF

:BROWSER 
	CALL make.bat =
	CALL make.bat python
	CALL make.bat -c
	CALL make.bat "$$BROWSER_PYSCRIPT"
	GOTO :EOF

:help
	@python -c "$$PRINT_HELP_PYSCRIPT" < %MAKEFILE_LIST%
	GOTO :EOF

:clean
	CALL make.bat clean-build
	CALL make.bat clean-pyc
	CALL make.bat clean-test
	GOTO :EOF

:clean-build
	DEL /Q build/ -fr
	DEL /Q dist/ -fr
	DEL /Q .eggs/ -fr
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	GOTO :EOF

:clean-pyc
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	GOTO :EOF

:clean-test
	DEL /Q .tox/ -fr
	DEL /Q .coverage /F
	DEL /Q htmlcov/ -fr
	DEL /Q .pytest_cache -fr
	GOTO :EOF

:lint
	flake8 vcfparser tests
	GOTO :EOF

:test
	py.test
	GOTO :EOF

:docs
	DEL /Q docs/vcfparser.rst /F
	DEL /Q docs/modules.rst /F
	sphinx-apidoc -o docs/ vcfparser
	
	CALL make.bat -C docs clean
	CALL make.bat -C docs html
	%BROWSER% docs/_build/html/index.html
	GOTO :EOF

:servedocs
	CALL make.bat docs
	watchmedo shell-command -p '*.rst' -c 'CALL make.bat -C docs html' -R -D .
	GOTO :EOF

:test_release
	CALL make.bat dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	GOTO :EOF

:release
	CALL make.bat dist
	twine upload dist/*
	GOTO :EOF

:dist
	CALL make.bat clean
	python setup.py sdist
	python setup.py bdist_wheel
	DIR dist /Q
	GOTO :EOF

:install
	CALL make.bat clean
	python setup.py install
	GOTO :EOF

:error
    IF "%1"=="" (
        ECHO make: *** No targets specified and no makefile found.  Stop.
    ) ELSE (
        ECHO make: *** No rule to make target '%1%'. Stop.
    )
    GOTO :EOF
