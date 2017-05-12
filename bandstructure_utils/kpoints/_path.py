#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from collections import namedtuple

import numpy as np
from fsc.export import export

from ..io._serialize_mapping import subscribe_serialize
from ..io import _hdf5_utils
from ..lattice import Lattice
from ._base import KpointsBase

@export
@subscribe_serialize('kpoints_path')
class KpointsPath(KpointsBase):
    """
    Defines a k-point path.

    """
    def __init__(self, *, paths, special_points={}, kpoint_distance=1e-3, unit_cell='auto'):
        self._paths = [
            [_Vertex(pt, special_points) for pt in single_path]
            for single_path in paths
        ]
        dimensions = set(
            pt.dimension
            for single_path in  self._paths
            for pt in single_path
        )
        if len(dimensions) != 1:
            raise ValueError('Inconsistent dimensions: {}'.format(dimensions))
        dim = dimensions.pop()
        if unit_cell == 'auto':
            uc = np.eye(dim)
        else:
            uc = np.array(unit_cell)
        if uc.shape != (dim, dim):
            raise ValueError('Inconsistent shape of the unit cell: {}, should be {}'.format(uc.shape, (dim, dim)))
        self._lattice = Lattice(matrix=uc)
        self._kpoint_distance = kpoint_distance
        self._evaluate_paths()

    def _evaluate_paths(self):
        self._kpoints_explicit = []
        self._labels = []
        for single_path in self._paths:
            self._evaluate_single_path(single_path)
        self._kpoints_explicit = np.array(self._kpoints_explicit)
        self._kpoints_explicit.flags.writeable = False

    def _evaluate_single_path(self, single_path):
        N = len(self._kpoints_explicit)
        self._kpoints_explicit.append(single_path[0].frac)
        self._labels.append(_KpointLabel(index=N, label=single_path[0].label))
        for start, end in zip(single_path, single_path[1:]):
            self._evaluate_line(start, end)

    def _evaluate_line(self, start, end):
        dist = self._lattice.get_reciprocal_cartesian_distance(start.frac, end.frac)
        npoints = max(int(np.round_(dist / self._kpoint_distance)) + 1, 2)
        steps = np.linspace(0, 1, npoints)[1:]
        kpoints = [(1 - s) * start.frac + s * end.frac for s in steps]
        self._kpoints_explicit.extend(kpoints)
        self._labels.append(_KpointLabel(
            index=len(self._kpoints_explicit) - 1,
            label=end.label
        ))

    @property
    def kpoints_explicit(self):
        return self._kpoints_explicit

    @property
    def labels(self):
        return self._labels

    def to_hdf5(self, hdf5_handle):
        path_labels = [
            [pt.label for pt in single_path]
            for single_path in self._paths
        ]
        _hdf5_utils._nested_list_to_hdf5(
            hdf5_handle.create_group('path_labels'), path_labels, str
        )
        special_points = {
            pt.label: pt.frac
            for special_path in self._paths for pt in special_path
        }
        _hdf5_utils._dict_to_hdf5(
            hdf5_handle.create_group('special_points'), special_points
        )
        hdf5_handle['kpoint_distance'] = self._kpoint_distance
        hdf5_handle['unit_cell'] = self._lattice.matrix

    @classmethod
    def from_hdf5(cls, hdf5_handle):
        path_labels = _hdf5_utils._nested_list_from_hdf5(hdf5_handle['path_labels'])
        special_points = _hdf5_utils._dict_from_hdf5(hdf5_handle['special_points'])
        kpoint_distance = hdf5_handle['kpoint_distance'].value
        unit_cell = hdf5_handle['unit_cell'].value

        return cls(
            paths=path_labels,
            special_points=special_points,
            kpoint_distance=kpoint_distance,
            unit_cell=unit_cell
        )

class _Vertex:
    def __init__(self, point, special_points):
        self.frac = np.array(special_points.get(point, point))
        self.label = str(point)

    @property
    def dimension(self):
        return self.frac.shape[0]

_KpointLabel = namedtuple('_KpointLabel', ['index', 'label'])
