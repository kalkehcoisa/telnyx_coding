#!/usr/bin/env python3
import io

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
import shlex
import sys


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


readme = io.open('README.md', 'r', encoding='utf-8').read()

setup(
    name='network',
    description='Telnyx challenge',
    long_description=readme,
    author='Jayme Tosi neto',
    author_email='kalkehcoisa@gmail.com',
    version='0.1.2.3.4.5',
    packages=find_packages(),
    tests_require=[
        'pytest==3.5.1',
        # 'pytest-mock>=1.6.3'
    ],
    cmdclass={'test': PyTest},
    # install_requires=[],
    entry_points="""
        [console_scripts]
        network=network.cli:cli_run
    """
)
