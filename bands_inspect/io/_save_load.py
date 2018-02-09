"""
Defines free functions to serialize / deserialize bands-inspect objects to HDF5.
"""

from fsc.hdf5_io import save, load, from_hdf5, from_hdf5_file, to_hdf5, to_hdf5_file

__all__ = [
    'save', 'load', 'from_hdf5', 'from_hdf5_file', 'to_hdf5', 'to_hdf5_file'
]
