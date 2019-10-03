# -*- coding: utf-8 -*-

# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the data class for explicitly specified k-points.
"""

import types

import numpy as np
from fsc.export import export
from fsc.hdf5_io import subscribe_hdf5

from ._base import KpointsBase


@export
@subscribe_hdf5(
    'bands_inspect.kpoints_explicit', extra_tags=('kpoints_explicit', )
)
class KpointsExplicit(KpointsBase, types.SimpleNamespace):
    """
    Defines an explicit set of k-points.

    :param kpoints: List of explicit k-points.
    :type kpoints: list
    """
    def __init__(self, kpoints):
        self.kpoints = np.array(kpoints)

    @property
    def kpoints_explicit(self):
        return self.kpoints

    def to_hdf5(self, hdf5_handle):
        hdf5_handle['kpoints'] = self.kpoints

    @classmethod
    def from_hdf5(cls, hdf5_handle):
        return cls(kpoints=hdf5_handle['kpoints'][()])
