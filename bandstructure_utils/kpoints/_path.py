#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import abc
import h5py
import numbers
import numpy as np

from fsc.export import export

from ..io._serialize_mapping import subscribe_serialize
from ._base import KpointsBase

@export
@subscribe_serialize('kpoints_path')
class KpointsPath(KpointsBase):
    """
    Defines a k-point path, with labelled vertices.

    :param vertices: Defines the special k-point vertices used in the path.
    :type vertices: dict

    :param path: List of vertices which are in the k-point path. By default, all vertices are connected. If two vertices should not be connected, add ``None`` between them.
    :type path: list

    :param points_per_line: Number of k-points in each line connecting two k-points. This can be either an integer (in which case all lines contain the same number of k-points, or a list of integers (corresponding to each line).
    :type points_per_line: int, list
    """
    def __init__(self, *, vertices, path, points_per_line=100):
        self.vertices = {str(label): np.array(kpt) for label, kpt in vertices.items()}
        self.path = [str(p) if p is not None else p for p in path]
        unknown_vertices = set(self.path) - self.vertices.keys() - {None}
        if unknown_vertices:
            raise ValueError("Unrecognized {} {} in 'path'. Vertices must be defined in the 'vertices' mapping.".format('vertex' if len(unknown_vertices) == 1 else 'vertices', ', '.join(str(x) for x in unknown_vertices)))
        if isinstance(points_per_line, numbers.Integral):
            self.points_per_line = [points_per_line] * (len(path) - 1)
        else:
            self.points_per_line = list(points_per_line)
        if len(self.points_per_line) != len(self.path) - 1:
            raise ValueError("Invalid number of entries in 'points_per_line': Found {}, should be {}".format(len(self.points_per_line), len(self.path) - 1))

    @property
    def kpoints_explicit(self):
        kpoints = []
        start_added = False
        for start, end, n_points in zip(self.path, self.path[1:], self.points_per_line):
            if start is None or end is None:
                start_added = False
                continue
            k_start = self.vertices[start]
            k_end = self.vertices[end]
            steps = np.linspace(0, 1, n_points)
            if start_added:
                steps = steps[1:]
            kpoints.extend([(1 - s) * k_start + s * k_end for s in steps])
            start_added = True
        return np.array(kpoints)

    def __iter__(self):
        return iter(self.kpoints_explicit)

    def __array__(self):
        return self.kpoints_explicit

    def to_hdf5(self, hdf5_handle):
        path_group = hdf5_handle.create_group('path')
        for i, p in enumerate(self.path):
            if p is None:
                path_group.create_dataset(str(i), dtype=h5py.special_dtype(vlen=str))
            else:
                path_group[str(i)] = p
        hdf5_handle['points_per_line'] = self.points_per_line
        vertices_group = hdf5_handle.create_group('vertices')
        for key, val in self.vertices.items():
            vertices_group[key] = val

    @classmethod
    def from_hdf5(cls, hdf5_handle):
        vertices_group = hdf5_handle['vertices']
        vertices_res = dict()
        for key in vertices_group:
            vertices_res[key] = vertices_group[key].value
        path_group = hdf5_handle['path']
        path_res = []
        for idx in sorted(path_group, key=int):
            g = path_group[idx]
            if g.shape is None:
                path_res.append(None)
            else:
                path_res.append(path_group[idx].value)
        return cls(
            vertices=vertices_res,
            path=path_res,
            points_per_line=hdf5_handle['points_per_line'].value
        )
