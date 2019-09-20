from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Kiran Bishwa",
    author_email='everestial01@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Minimaistic VCf parser in python",
    install_requires=requirements,
    license="MIT license",
    long_description=readme ,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='vcfparser',
    name='vcfparser',
    packages=find_packages(include=['vcfparser']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/everestial/vcfparser',
    version='0.1.6',
    zip_safe=False,
)

