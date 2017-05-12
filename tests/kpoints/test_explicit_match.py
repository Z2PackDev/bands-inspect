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
    (KpointsPath(special_points=VERTICES, paths=[['a', 'b', 'c']], kpoint_distance=6), [[0, 0], [0.5, 0.5], [0.5, 0]]),
    (KpointsPath(special_points=VERTICES, paths=[['a', 'b', 'c']], kpoint_distance=2), [[0, 0], [0.25, 0.25], [0.5, 0.5], [0.5, 0.25], [0.5, 0]]),
    (KpointsPath(special_points=VERTICES, paths=[['a', 'b', 'c']], kpoint_distance=2.5), [[0, 0], [0.25, 0.25], [0.5, 0.5], [0.5, 0]]),
]

@pytest.mark.parametrize('instance, reference', INSTANCES_EXPLICIT_KPOINTS)
def test_kpoints_explicit(instance, reference):
    assert_equal(instance.kpoints_explicit, reference)
