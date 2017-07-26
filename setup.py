#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages

import sys
if sys.version_info < (3, 4):
    raise 'must use Python version 3.4 or higher'

readme = """Utilities for creating, comparing and plotting bandstructures of materials."""

with open('./bands_inspect/_version.py', 'r') as f:
    match_expr = "__version__[^'" + '"]+([' + "'" + r'"])([^\1]+)\1'
    version = re.search(match_expr, f.read()).group(2)

setup(
    name='bands-inspect',
    version=version,
    url='http://z2pack.ethz.ch/bands-inspect',
    author='Dominik Gresch',
    author_email='greschd@gmx.ch',
    description=readme,
    install_requires=['numpy', 'scipy', 'matplotlib', 'h5py', 'click', 'decorator', 'fsc.export'],
    extras_require={'test': ['pytest', 'pytest-cov']},
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
        'Development Status :: 3 - Alpha'
    ],
    entry_points='''
        [console_scripts]
        bands_inspect=bands_inspect._cli:cli
    ''',
    license='GPL',
    packages=['bands_inspect', 'bands_inspect.kpoints', 'bands_inspect.io', 'bands_inspect.compare']
)
