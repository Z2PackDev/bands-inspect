#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import pytest
import numpy as np
from numpy.testing import assert_equal

from bandstructure_utils.kpoints import *

VERTICES = {'a': [0, 0], 'b': [0.5, 0.5], 'c': [0.5, 0]}

INSTANCES_EXPLICIT_KPOINTS = [
    (KpointsExplicit([[0.1, 0.3, 0.2], [0.9, 0.7, -0.1]]), [[0.1, 0.3, 0.2], [0.9, 0.7, -0.1]]),
    (KpointsMesh(mesh=[2, 2]), [[0, 0], [0, 0.5], [0.5, 0], [0.5, 0.5]]),
    (KpointsMesh(mesh=[2, 2], offset=[0.1, -0.1]), [[0.1, 0.9], [0.1, 0.4], [0.6, 0.9], [0.6, 0.4]]),
    (KpointsPath(vertices=VERTICES, paths=[['a', 'b', 'c']], points_per_line=2), [[0, 0], [0.5, 0.5], [0.5, 0]]),
    (KpointsPath(vertices=VERTICES, paths=[['a', 'b'], ['c', 'a']], points_per_line=2), [[0, 0], [0.5, 0.5], [0.5, 0], [0, 0]]),
    (KpointsPath(vertices=VERTICES, paths=[['a', 'b', 'c']], points_per_line=3), [[0, 0], [0.25, 0.25], [0.5, 0.5], [0.5, 0.25], [0.5, 0]]),
    (
        KpointsPath.from_lattice(
            lattice=[[1, 0], [0, 2]],
            vertices=VERTICES,
            paths=[['a', 'b', 'c']],
            total_num_points=4
        ),
        [[0, 0], [0.25, 0.25], [0.5, 0.5], [0.5, 0]]
    ),
    (
        KpointsPath.from_lattice(
            lattice=[[1, 0], [0, 1]],
            vertices=VERTICES,
            paths=[['a', 'b', 'c']],
            total_num_points=3
        ),
        [[0, 0], [0.5, 0.5], [0.5, 0]]
    ),
]

@pytest.mark.parametrize('instance, reference', INSTANCES_EXPLICIT_KPOINTS)
def test_kpoints_explicit(instance, reference):
    assert_equal(instance.kpoints_explicit, reference)
