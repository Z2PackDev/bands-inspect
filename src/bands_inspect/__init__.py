# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <mail@greschd.ch>
"""
A tool for modifying, comparing and plotting electronic bandstructures.
"""

import importlib.metadata

from . import kpoints
from . import eigenvals
from . import compare
from . import lattice
from . import plot

__version__ = importlib.metadata.version(__name__.replace(".", "-"))

__all__ = ("kpoints", "eigenvals", "compare", "lattice", "plot")
