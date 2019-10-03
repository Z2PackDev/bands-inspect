# -*- coding: utf-8 -*-

# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the base class for k-point data classes.
"""

import abc

from fsc.export import export
from fsc.hdf5_io import HDF5Enabled


@export
class KpointsBase(HDF5Enabled):
    """
    Base class for classes defining sets of k-points.
    """
    @abc.abstractproperty
    def kpoints_explicit(self):
        """
        Array containing all k-points explicitly.
        """
    def __iter__(self):
        return iter(self.kpoints_explicit)

    def __array__(self):
        return self.kpoints_explicit
