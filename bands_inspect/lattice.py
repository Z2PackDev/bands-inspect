#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import numpy as np
import scipy.linalg as la
from fsc.export import export

# TODO: move to a separate module

@export
class Lattice:
    def __init__(self, matrix):
        self.matrix = np.array(matrix)

    def __array__(self):
        return self.matrix

    @property
    def reciprocal_lattice(self):
        return type(self)(matrix=2 * np.pi * la.inv(self.matrix).T)

    def get_cartesian_coords(self, fractional_coords):
        return np.dot(fractional_coords, self.matrix)

    def get_fractional_coords(self, cartesian_coords):
        return la.solve(self.uc.T, np.array(cartesian_coords).T).T

    def get_cartesian_distance(self, fractional_coord_1, fractional_coord_2):
        return la.norm(
            self.get_cartesian_coords(fractional_coord_1) - self.get_cartesian_coords(fractional_coord_2)
        )

    def get_reciprocal_cartesian_distance(self, reciprocal_fractional_coord_1, reciprocal_fractional_coord_2):
        return self.reciprocal_lattice.get_cartesian_distance(reciprocal_fractional_coord_1, reciprocal_fractional_coord_2)
