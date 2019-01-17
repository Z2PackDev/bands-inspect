# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for loading old versions of the HDF5 format.
"""

import bands_inspect as bi


def test_legacy_path_eigenvals(sample):
    bi.io.load(sample('legacy_path_eigenvals.hdf5'))
