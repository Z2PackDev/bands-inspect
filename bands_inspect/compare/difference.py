#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import numpy as np
from fsc.export import export

@export
def general(
        eigenvals1, eigenvals2,
        *,
        avg_func=np.average,
        weight_eigenval=np.ones_like,
        symmetric_eigenval_weights=True,
        weight_kpoint=lambda kpts: np.ones(np.array(kpts).shape[0])
    ):

    kpoints = np.array(eigenvals1.kpoints)
    if not np.allclose(kpoints, np.array(eigenvals2.kpoints)):
        raise ValueError('The k-points of the two sets of eigenvalues do not match.')
    kpoint_weights = weight_kpoint(kpoints)
    if symmetric_eigenval_weights:
        eigenval_weights = np.mean(
            [
                weight_eigenval(eigenvals1.eigenvals),
                weight_eigenval(eigenvals2.eigenvals)
            ],
            axis=0
        )
    else:
        eigenval_weights = weight_eigenval(eigenvals1.eigenvals)

    weights = (eigenval_weights.T * kpoint_weights).T
    diff = np.abs(eigenvals1.eigenvals - eigenvals2.eigenvals)
    return avg_func(diff, weights=weights)

@export
def energy_window(
        *args,
        energy_window,
        **kwargs
    ):
    lower, upper = sorted(energy_window)
    def weight_eigenval(eigenvals):
        return np.array(
            np.logical_and(lower < eigenvals, eigenvals < upper),
            dtype=int
        )
    return general(*args, weight_eigenval=weight_eigenval, **kwargs)

@export
def select_bands(
        *args,
        bands,
        **kwargs
    ):
    bands = list(bands)
    def weight_eigenval(eigenvals):
        return np.array([
            [int(i in bands) for i, _ in enumerate(ev)]
            for ev in eigenvals
        ])
    return general(*args, weight_eigenval=weight_eigenval, **kwargs)
