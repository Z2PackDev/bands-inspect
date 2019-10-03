# -*- coding: utf-8 -*-

# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines a crystal lattice class.
"""

import numpy as np
import scipy.linalg as la
from fsc.export import export

# TODO: move to a separate module  # pylint: disable=fixme,useless-suppression


@export
class Lattice:
    """
    Defines a periodic lattice.
    """
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
        return la.solve(self.matrix.T, np.array(cartesian_coords).T).T

    def get_cartesian_distance(self, fractional_coord_1, fractional_coord_2):
        return la.norm(
            self.get_cartesian_coords(fractional_coord_1) -
            self.get_cartesian_coords(fractional_coord_2)
        )

    def get_reciprocal_cartesian_distance(  # pylint: disable=invalid-name
        self, reciprocal_fractional_coord_1, reciprocal_fractional_coord_2
    ):
        return self.reciprocal_lattice.get_cartesian_distance(
            reciprocal_fractional_coord_1, reciprocal_fractional_coord_2
        )
