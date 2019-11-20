# -*- coding: utf-8 -*-

# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the data container for eigenvalue data (bandstructures).
"""

import types

import numpy as np
from fsc.export import export
from fsc.hdf5_io import HDF5Enabled, subscribe_hdf5

from .kpoints import KpointsExplicit, KpointsBase
from .io import from_hdf5


@export
@subscribe_hdf5(
    'bands_inspect.eigenvals_data', extra_tags=('eigenvals_data', )
)
class EigenvalsData(HDF5Enabled, types.SimpleNamespace):
    """
    Data container for the eigenvalues at a given set of k-points. The eigenvalues are automatically sorted by value.

    :param kpoints: List of k-points where the eigenvalues are given.
    :type kpoints: list

    :param eigenvals: Eigenvalues at each k-point. The outer axis corresponds to the different k-points, and the inner axis corresponds to the different eigenvalues at a given k-point.
    :type eigenvals: 2D array
    """
    def __init__(self, *, kpoints, eigenvals):
        if not isinstance(kpoints, KpointsBase):
            kpoints = KpointsExplicit(kpoints)

        eigenvals = np.sort(eigenvals)
        if len(kpoints.kpoints_explicit) != len(eigenvals):
            raise ValueError(
                "Number of kpoints ({}) does not match the number of eigenvalue lists ({})"
                .format(len(kpoints.kpoints_explicit), len(eigenvals))
            )
        self.kpoints = kpoints
        self.eigenvals = eigenvals

    def slice_bands(self, band_idx):
        """
        Returns a new instance which contains only the bands given in the index.

        :param band_idx: Indices for the bands in the new instance.
        :type band_idx: list
        """
        new_eigenvals = self.eigenvals.T[sorted(band_idx)].T
        return type(self)(kpoints=self.kpoints, eigenvals=new_eigenvals)

    @classmethod
    def from_eigenval_function(
        cls, *, kpoints, eigenval_function, listable=False
    ):
        """
        Create an instance using a function that calculates the eigenvalues.

        :param kpoints: k-points for which the eigenvalues are to be calculated.
        :type kpoints: KpointsBase

        :param eigenval_function: Function which calculates the eigenvalues.

        :param listable: Flag showing whether the function can handle a list of k-points (``True``) or only single k-points (``False``).
        :type listable: bool
        """
        if listable:
            eigenvals = eigenval_function(kpoints.kpoints_explicit)
        else:
            eigenvals = [
                eigenval_function(k) for k in kpoints.kpoints_explicit
            ]
        return cls(kpoints=kpoints, eigenvals=eigenvals)

    def to_hdf5(self, hdf5_handle):
        hdf5_handle.create_group('kpoints_obj')
        self.kpoints.to_hdf5(hdf5_handle['kpoints_obj'])
        hdf5_handle['eigenvals'] = self.eigenvals

    @classmethod
    def from_hdf5(cls, hdf5_handle):
        kpoints = from_hdf5(hdf5_handle['kpoints_obj'])
        eigenvals = hdf5_handle['eigenvals'][()]
        return cls(kpoints=kpoints, eigenvals=eigenvals)

    def shift(self, value):
        """
        Returns an instance with eigenvalues shifted by the given value.

        :param value: The value by which the eigenvalues are shifted.
        :type value: float
        """
        new_eigenvals = self.eigenvals + value
        return type(self)(kpoints=self.kpoints, eigenvals=new_eigenvals)
