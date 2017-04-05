#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import itertools

import numpy as np
from fsc.export import export

from .base import KpointsBase

@export
class KpointsMesh:
    def __init__(self, mesh, offset=None):
        self.mesh = tuple(int(m) for m in mesh)
        if offset is None:
            self.offset = np.zeros_like(self.mesh)
        else:
            self.offset = np.array(offset)

        if len(self.offset) != len(self.mesh):
            raise ValueError(
                "Length of 'offset' ({}) does not match the length of 'mesh' ({}).".format(
                    len(self.offset), len(self.mesh)
                )
            )
        self.offset = offset or np.array(offset)

    @property
    def kpoints_explicit(self):
        res = np.array(list(itertools.product(*[
            np.linspace(0, 1, m, endpoint=False) for m in self.mesh
        ])))
        res += self.offset
        res.flags.writeable = False
        return res
