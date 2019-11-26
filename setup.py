from setuptools import setup, find_packages
from setuptools import Extension
from Cython.Build import cythonize



with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = ['pytest-runner', 'Cython']

test_requirements = ['pytest', ]

# extensions = [Extension(['vcfparser/*.pyx']]

setup(
    author="Kiran Bishwa",
    author_email='everestial007@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    description="Minimaistic VCf parser in python",
    install_requires=requirements,
    license="MIT license",
    long_description=readme ,
    include_package_data=True,
    keywords='vcfparser',
    name='vcfparser',
    packages=find_packages(),    
    ext_modules = cythonize(['vcfparser/*.pyx']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/everestial/vcfparser',
    version='0.2.0',
    zip_safe=False,
)

