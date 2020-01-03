.. highlight:: shell

============
Contributing
============

Contributions are welcome and they are greatly appreciated! Every little bit
helps and credit will always be given.

As a general guideline, every Financial Mathematics implementation should be
mathematically sounded and comprehensively documented, as to make sure
every routine implemented could, in thesis, be reproduced with paper and
pencil.

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/yanomateus/loan-calculator/issues.

If you are reporting a bug, please include:

* You python, numpy and scipy versions.
* A minimal, reproducible scenario.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Loan Calculator could always use more documentation, whether as part of the
official Loan Calculator docs, in docstrings, or even on the web in blog posts,
articles, and such. Any improvement in the mathematical description of the
implemented features are particularly wanted.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/yanomateus/loan-calculator/issues.

If you are proposing a feature:

* Explain in detail how it would work. If it is an implementation of any
  Financial Mathematics feature, please make sure to comprehensively document
  the Mathematics behind it.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `loan-calculator` for local development.

1. Fork the `loan-calculator` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/loan-calculator.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv loan-calculator
    $ cd loan-calculator/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 loan-calculator tests
    $ python setup.py test or pytest
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub.

7. Submit a pull request through the GitHub website with a description of
   your changes.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.7, 3.6, 3.7 and 3.8, and for PyPy.
   Check https://travis-ci.org/yanomateus/loan-calculator/pull_requests
   and make sure that the tests pass for all supported Python versions.

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags

Travis will then deploy to PyPI if tests pass.
