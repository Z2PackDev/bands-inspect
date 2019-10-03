# -*- coding: utf-8 -*-

# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Usage: pip install .[test,doc,dev]
"""

import os
import re
import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 4):
    raise 'must use Python version 3.4 or higher'

README = """Utilities for creating, comparing and plotting bandstructures of materials."""

with open('./bands_inspect/__init__.py', 'r') as f:
    MATCH_EXPR = "__version__[^'\"]+(['\"])([^'\"]+)"
    VERSION = re.search(MATCH_EXPR, f.read()).group(2).strip()

EXTRAS_REQUIRE = {
    'test': ['pytest', 'pytest-cov'],
    'doc':
    ['sphinx', 'sphinx-rtd-theme', 'sphinx-click', 'ipython>=6.2', 'tbmodels'],
    'pre-commit': [
        'pre-commit==1.18.3', 'yapf==0.28.0', 'prospector==1.1.7',
        'pylint==2.3.1'
    ]
}
EXTRAS_REQUIRE['dev'] = sum(EXTRAS_REQUIRE.values(), [])

INSTALL_REQUIRES = ['click', 'decorator', 'fsc.export']
if os.environ.get('READTHEDOCS') != 'True':
    INSTALL_REQUIRES += [
        'numpy', 'scipy', 'matplotlib>=2', 'h5py', 'fsc.hdf5-io'
    ]

setup(
    name='bands-inspect',
    version=VERSION,
    url='http://z2pack.ethz.ch/bands-inspect',
    author='Dominik Gresch',
    author_email='greschd@gmx.ch',
    description=README,
    long_description=README,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English', 'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Development Status :: 4 - Beta'
    ],
    entry_points='''
        [console_scripts]
        bands-inspect=bands_inspect._cli:cli
    ''',
    license='Apache 2.0',
    packages=find_packages()
)
