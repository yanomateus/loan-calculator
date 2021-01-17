# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('LICENSE') as license_file:
    license_ = license_file.read()


setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Mateus Yano",
    author_email='yano.mateus@gmail.com',
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Loan Calculator",
    install_requires=[],
    license="MIT license",
    long_description=readme + '\n\n' + history + '\n\n' + license_,
    include_package_data=True,
    keywords='loan_calculator',
    name='loan_calculator',
    packages=find_packages(include=['loan_calculator', 'loan_calculator.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/yanomateus/loan-calculator',
    version='1.2.0',
    zip_safe=False,
)
