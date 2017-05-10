#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import abc
import numbers
import numpy as np

from fsc.export import export

from ..io._serialize_mapping import subscribe_serialize
from ..io import _hdf5_utils
from ._base import KpointsBase

@export
@subscribe_serialize('kpoints_path')
class KpointsPath(KpointsBase):
    """
    Defines a k-point path, with labelled vertices.

    :param vertices: Defines the special k-point vertices used in the path.
    :type vertices: dict

    :param paths: List of k-point paths. Each k-point path is a list of vertices. Only vertices within the same path are connected.
    :type paths: list

    :param points_per_line: Number of k-points in each line connecting two k-points. This can be either an integer (in which case all lines contain the same number of k-points, or a nested list of integers (corresponding to each line).
    :type points_per_line: int, list
    """
    def __init__(self, *, vertices, paths, points_per_line=100):
        self.vertices = {str(label): np.array(kpt) for label, kpt in vertices.items()}
        self.paths = [[str(p) for p in single_path] for single_path in paths]
        all_vertices = set()
        for path in self.paths:
            all_vertices.update(path)
        unknown_vertices = all_vertices - self.vertices.keys()
        if unknown_vertices:
            raise ValueError("Unrecognized {} {} in 'path'. Vertices must be defined in the 'vertices' mapping.".format('vertex' if len(unknown_vertices) == 1 else 'vertices', ', '.join(str(x) for x in unknown_vertices)))
        if isinstance(points_per_line, numbers.Integral):
            self.points_per_line = [
                [points_per_line] * (len(single_path) - 1)
                for single_path in self.paths
            ]
        else:
            self.points_per_line = list(points_per_line)
        for single_path, path_num_points in zip(self.paths, self.points_per_line):
            if len(single_path) < 2:
                raise ValueError('Each individual k-point path must have at least 2 vertices.')
            if len(single_path) != len(path_num_points) + 1:
                raise ValueError("Invalid number of entries in 'points_per_line'.")
            if any(num_points < 2 for num_points in path_num_points):
                raise ValueError("The number of k-points in each line must be at least 2.")

    @property
    def kpoints_explicit(self):
        kpoints = []
        for single_path, path_num_points in zip(self.paths, self.points_per_line):
            kpoints.extend(self._path_kpoints(single_path, path_num_points))
        return np.array(kpoints)

    def _path_kpoints(self, path, num_kpoints):
        kpoints = [self.vertices[path[0]]]
        for start, end, n_points in zip(path, path[1:], num_kpoints):
            steps = np.linspace(0, 1, n_points)[1:]
            k_start = self.vertices[start]
            k_end = self.vertices[end]
            kpoints.extend([(1 - s) * k_start + s * k_end for s in steps])
        return kpoints

    def to_hdf5(self, hdf5_handle):
        _hdf5_utils._nested_list_to_hdf5(
            hdf5_handle.create_group('paths'), self.paths, str
        )
        _hdf5_utils._nested_list_to_hdf5(
            hdf5_handle.create_group('points_per_line'), self.points_per_line
        )
        _hdf5_utils._dict_to_hdf5(
            hdf5_handle.create_group('vertices'), self.vertices
        )

    @classmethod
    def from_hdf5(cls, hdf5_handle):
        paths = _hdf5_utils._nested_list_from_hdf5(hdf5_handle['paths'])
        points_per_line = _hdf5_utils._nested_list_from_hdf5(hdf5_handle['points_per_line'])
        vertices = _hdf5_utils._dict_from_hdf5(hdf5_handle['vertices'])

        return cls(
            vertices=vertices,
            paths=paths,
            points_per_line=points_per_line
        )
