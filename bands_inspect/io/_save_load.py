# -*- coding: utf-8 -*-

# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines free functions to serialize / deserialize bands-inspect objects to HDF5.
"""

from fsc.hdf5_io import save, load, from_hdf5, from_hdf5_file, to_hdf5, to_hdf5_file

__all__ = [
    'save', 'load', 'from_hdf5', 'from_hdf5_file', 'to_hdf5', 'to_hdf5_file'
]
