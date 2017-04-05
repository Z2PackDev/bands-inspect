#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from bandstructure_utils.kpoints import *
from bandstructure_utils.eigenvals import *

KPOINTS_INSTANCES = [
    KpointsExplicit([[0.1, 0.5, 0.2], [0.9, 0.3, 0.5]]),
    KpointsMesh([2, 5, 2], offset=[0.1, -0.3, 0.4]),
    KpointsMesh([1, 2, 3]),
]

EIGENVALS_INSTANCES = [
    EigenvalsData(
        kpoints=[[0.1, 0.2, 0.3], [0.5, 0.1, 0.3]],
        eigenvals=[[-0.2, 0.3, 0.4, 5], [-0.5, -0.7, 1, 9]]
    )
]

SERIALIZABLE_INSTANCES = KPOINTS_INSTANCES + EIGENVALS_INSTANCES
