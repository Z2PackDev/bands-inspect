# -*- coding: utf-8 -*-

# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the data class for a regular k-point mesh.
"""

import types
import itertools

import numpy as np
from fsc.export import export
from fsc.hdf5_io import subscribe_hdf5

from ._base import KpointsBase


@export
@subscribe_hdf5('bands_inspect.kpoints_mesh', extra_tags=('kpoints_mesh', ))
class KpointsMesh(KpointsBase, types.SimpleNamespace):
    r"""
    Defines k-points on a regular mesh.

    :param mesh: Defines the grid size (number of different k-point values) for each dimension.
    :type mesh: list

    :param offset: Offset added to the k-point values. If nothing is given, the grid is aligned at the :math:`\Gamma` - point.
    :type offset: list
    """
    def __init__(self, mesh, offset=None):
        mesh = tuple(int(m) for m in mesh)
        if offset is None:
            offset = np.zeros_like(mesh)
        else:
            offset = np.array(offset)

        if len(offset) != len(mesh):
            raise ValueError(
                "Length of 'offset' ({}) does not match the length of 'mesh' ({})."
                .format(offset, mesh)
            )
        self.mesh = mesh
        self.offset = offset

    @property
    def kpoints_explicit(self):
        res = np.array(
            list(
                itertools.product(
                    *[np.linspace(0, 1, m, endpoint=False) for m in self.mesh]
                )
            )
        )
        res += self.offset
        res %= 1
        res.flags.writeable = False
        return res

    def to_hdf5(self, hdf5_handle):
        hdf5_handle['mesh'] = self.mesh
        hdf5_handle['offset'] = self.offset

    @classmethod
    def from_hdf5(cls, hdf5_handle):
        return cls(
            mesh=hdf5_handle['mesh'][()], offset=hdf5_handle['offset'][()]
        )
