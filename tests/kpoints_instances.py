#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from bandstructure_utils.kpoints import *

KPOINTS_INSTANCES = [
    KpointsExplicit([[0.1, 0.5, 0.2], [0.9, 0.3, 0.5]]),
    KpointsMesh([2, 5, 2], offset=[0.1, -0.3, 0.4]),
    KpointsMesh([1, 2, 3]),
]
