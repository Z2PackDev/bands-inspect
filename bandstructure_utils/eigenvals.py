#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from collections import namedtuple

import numpy as np
from fsc.export import export

from ._serializable import Serializable
from .kpoints import KpointsExplicit
from .kpoints.base import KpointsBase
from .io import from_hdf5
from .io._serialize_mapping import subscribe_serialize

@export
@subscribe_serialize('eigenvals_data')
# Note: namedtuple inheritance breaks the check for abstract methods
class EigenvalsData(Serializable, namedtuple('EigenvalsBase', ['kpoints', 'eigenvals'])):
    def __new__(cls, *, kpoints, eigenvals):
        if not isinstance(kpoints, KpointsBase):
            kpoints = KpointsExplicit(kpoints)

        eigenvals = np.array(eigenvals)
        if len(kpoints.kpoints_explicit) != len(eigenvals):
            raise ValueError(
                "Number of kpoints ({}) does not match the number of eigenvalue lists ({})".format(
                    len(kpoints.kpoints_explicit), len(eigenvals)
                )
            )
        return super().__new__(cls, kpoints, eigenvals)

    @classmethod
    def from_eigenval_function(cls, *, kpoints, eigenval_function, listable=False):
        if listable:
            eigenvals = eigenval_function(kpoints.kpoints_explicit)
        else:
            eigenvals = [eigenval_function(k) for k in kpoints.kpoints_explicit]
        return cls(kpoints=kpoints, eigenvals=eigenvals)

    def to_hdf5(self, hdf5_handle):
        hdf5_handle.create_group('kpoints_obj')
        self.kpoints.to_hdf5(hdf5_handle['kpoints_obj'])
        hdf5_handle['eigenvals'] = self.eigenvals

    @classmethod
    def from_hdf5(cls, hdf5_handle):
        kpoints = from_hdf5(hdf5_handle['kpoints_obj'])
        eigenvals = hdf5_handle['eigenvals'].value
        return cls(kpoints=kpoints, eigenvals=eigenvals)
