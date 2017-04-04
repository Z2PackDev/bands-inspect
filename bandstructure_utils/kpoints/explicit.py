#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import numpy as np
from fsc.export import export

from .base import KpointSet

@export
class ExplicitKpoints(KpointSet):
    def __init__(self, kpoints):
        self._kpoints = np.array(kpoints)

    @property
    def explicit_kpoints(self):
        return self._kpoints

    def to_hdf5(self, hdf5_handle):
        hdf5_handle['kpoints'] = self._kpoints

    @classmethod
    def from_hdf5(cls, hdf5_handle):
        return cls(kpoints=hdf5_handle['kpoints'].value)
