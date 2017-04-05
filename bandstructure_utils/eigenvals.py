#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from collections import namedtuple

import numpy as np

from .kpoints import KpointsExplicit
from .kpoints.base import KpointsBase

class EigenvalsData(namedtuple('EigenvalsBase', ['kpoints', 'eigenvals'])):
    def __new__(cls, *, kpoints, eigenvals):
        if not isinstance(kpoints, KpointsBase):
            kpoints = KpointsExplicit(kpoints)

        eigenvals = np.array(eigenvals)
        if len(kpoints.kpoints_explicit) != len(eigenvals):
            raise ValueError(
                "Number of kpoints ({}) does not match the number of eigenvalue lists ({})".format(
                    len(kpoints.kpoints_explicit), len(eigenvals)
                )
            )
        return super().__new__(cls, kpoints, eigenvals)

    @classmethod
    def from_eigenval_function(cls, *, kpoints, eigenval_function, listable=False):
        if listable:
            eigenval = eigenval_function(kpoints.kpoints_explicit)
        else:
            eigenval = [eigenval_function(k) for k in kpoints.kpoints_explicit]
        return cls(kpoints=kpoints, eigenval=eigenval)
