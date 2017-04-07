#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import types

import numpy as np
from fsc.export import export

from ..io._serialize_mapping import subscribe_serialize
from . import KpointsBase

@export
@subscribe_serialize('kpoints_explicit')
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
        return cls(kpoints=hdf5_handle['kpoints'].value)
