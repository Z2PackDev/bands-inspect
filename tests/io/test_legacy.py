# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <mail@greschd.ch>
"""
Tests for loading old versions of the HDF5 format.
"""

import bands_inspect as bi


def test_legacy_path_eigenvals(sample):
    bi.io.load(sample("legacy_path_eigenvals.hdf5"))
