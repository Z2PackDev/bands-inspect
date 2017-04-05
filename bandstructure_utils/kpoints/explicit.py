#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import numpy as np
from fsc.export import export

from ..io._serialize_mapping import subscribe_serialize
from . import KpointsBase

@export
@subscribe_serialize('kpoints_explicit')
class KpointsExplicit(KpointsBase):
    def __init__(self, kpoints):
        self._kpoints = np.array(kpoints)
        self._kpoints.flags.writeable = False

    @property
    def kpoints_explicit(self):
        return self._kpoints

    def to_hdf5(self, hdf5_handle):
        hdf5_handle['kpoints'] = self._kpoints

    @classmethod
    def from_hdf5(cls, hdf5_handle):
        return cls(kpoints=hdf5_handle['kpoints'].value)
