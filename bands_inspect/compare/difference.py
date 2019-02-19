# -*- coding: utf-8 -*-

# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines functions to compare two bandstructures by calculating their difference, with different averaging and weighting methods.
"""

import numpy as np
from fsc.export import export


@export
def calculate(
    eigenvals1,
    eigenvals2,
    *,
    avg_func=np.average,
    weight_eigenval=np.ones_like,
    symmetric_eigenval_weights=True,
    weight_kpoint=lambda kpts: np.ones(np.array(kpts).shape[0])
):
    """
    Calculate the difference between two bandstructures.

    :param eigenvals1: The first set of eigenvalues.
    :type eigenvals1: EigenvalsData

    :param eigenvals2: The second set of eigenvalues.
    :type eigenvals2: EigenvalsData

    :param avg_func: Function which is used to average the difference between the two sets of eigenvalues.

    :param weight_eigenval: A function which takes the eigenvalues as input, and returns the corresponding weights.

    :param symmetric_eigenval_weights: Determines whether both sets of eigenvalues are used to calculate weights, or just the first one.
    :type symmetric_eigenval_weights: bool

    :param weight_kpoint: A function which takes the k-points as input, and returns the corresponding weights.
    """
    kpoints = np.array(eigenvals1.kpoints)
    if not np.allclose(kpoints, np.array(eigenvals2.kpoints)):
        raise ValueError(
            'The k-points of the two sets of eigenvalues do not match.'
        )
    kpoint_weights = weight_kpoint(kpoints)
    if symmetric_eigenval_weights:
        eigenval_weights = np.mean([
            weight_eigenval(eigenvals1.eigenvals),
            weight_eigenval(eigenvals2.eigenvals)
        ],
                                   axis=0)
    else:
        eigenval_weights = weight_eigenval(eigenvals1.eigenvals)

    weights = (eigenval_weights.T * kpoint_weights).T
    diff = np.abs(eigenvals1.eigenvals - eigenvals2.eigenvals)
    return avg_func(diff, weights=weights)


@export
def energy_window(lower, upper):
    """
    Creates an eigenvalue weighting function that only takes into account eigenvalues in a certain energy window.

    :param lower: Lower bound of the energy window.
    :type lower: float

    :param upper: Upper bound of the energy window.
    :type upper: float
    """
    lower, upper = sorted([lower, upper])

    def weight_eigenval(eigenvals):
        return np.array(
            np.logical_and(lower < eigenvals, eigenvals < upper), dtype=int
        )

    return weight_eigenval
