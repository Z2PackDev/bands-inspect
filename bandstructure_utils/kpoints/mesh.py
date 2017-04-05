#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import itertools
from collections import namedtuple

import numpy as np
from fsc.export import export

from ..io._serialize_mapping import subscribe_serialize
from . import KpointsBase

@export
@subscribe_serialize('kpoints_mesh')
# Note: namedtuple inheritance breaks the check for abstract methods
class KpointsMesh(KpointsBase, namedtuple('MeshBase', ['mesh', 'offset'])):
    def __new__(cls, mesh, offset=None):
        mesh = tuple(int(m) for m in mesh)
        if offset is None:
            offset = np.zeros_like(mesh)
        else:
            offset = np.array(offset)

        if len(offset) != len(mesh):
            raise ValueError(
                "Length of 'offset' ({}) does not match the length of 'mesh' ({}).".format(
                    len(offset), len(mesh)
                )
            )
        return super().__new__(
            cls,
            mesh=mesh,
            offset=offset
        )

    @property
    def kpoints_explicit(self):
        res = np.array(list(itertools.product(*[
            np.linspace(0, 1, m, endpoint=False) for m in self.mesh
        ])))
        res += self.offset
        res %= 1
        res.flags.writeable = False
        return res

    def to_hdf5(self, hdf5_handle):
        hdf5_handle['mesh'] = self.mesh
        hdf5_handle['offset'] = self.offset

    @classmethod
    def from_hdf5(cls, hdf5_handle):
        return cls(mesh=hdf5_handle['mesh'].value, offset=hdf5_handle['offset'].value)
