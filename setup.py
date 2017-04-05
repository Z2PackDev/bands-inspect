#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    20.10.2014 11:27:40 CEST
# File:    setup.py

import re
from setuptools import setup, find_packages

import sys
if sys.version_info < (3, 4):
    raise 'must use Python version 3.4 or higher'

readme = """Utilities for creating, comparing and plotting bandstructures of materials."""

with open('./bandstructure_utils/_version.py', 'r') as f:
    match_expr = "__version__[^'" + '"]+([' + "'" + r'"])([^\1]+)\1'
    version = re.search(match_expr, f.read()).group(2)

setup(
    name='bandstructure-utils',
    version=version,
    url='http://z2pack.ethz.ch/bandstructure-utils',
    author='Dominik Gresch',
    author_email='greschd@gmx.ch',
    description=readme,
    install_requires=['numpy', 'fsc.export', 'h5py', 'decorator'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Development Status :: 4 - Beta'
    ],
    license='GPL',
    packages=['bandstructure_utils', 'bandstructure_utils.kpoints', 'bandstructure_utils.io']
)
