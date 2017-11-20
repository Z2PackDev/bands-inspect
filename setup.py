"""
Usage: pip install .[test,doc,dev]
"""

import re
import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 4):
    raise 'must use Python version 3.4 or higher'

README = """Utilities for creating, comparing and plotting bandstructures of materials."""

with open('./bands_inspect/_version.py', 'r') as f:
    MATCH_EXPR = "__version__[^'" + '"]+([' + "'" + r'"])([^\1]+)\1'
    VERSION = re.search(MATCH_EXPR, f.read()).group(2)

EXTRAS_REQUIRE = {
    'test': ['pytest', 'pytest-cov'],
    'doc': ['sphinx', 'sphinx-rtd-theme'],
    'dev': ['pre-commit', 'yapf', 'prospector']
}
EXTRAS_REQUIRE['dev'] += EXTRAS_REQUIRE['test'] + EXTRAS_REQUIRE['doc']

setup(
    name='bands-inspect',
    version=VERSION,
    url='http://z2pack.ethz.ch/bands-inspect',
    author='Dominik Gresch',
    author_email='greschd@gmx.ch',
    description=README,
    install_requires=[
        'numpy', 'scipy', 'matplotlib', 'h5py', 'click', 'decorator',
        'fsc.export'
    ],
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English', 'Operating System :: Unix',
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
        bands-inspect=bands_inspect._cli:cli
    ''',
    license='GPL',
    packages=find_packages()
)
