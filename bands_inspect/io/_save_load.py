#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import h5py
from fsc.export import export

from ._serialize_mapping import SERIALIZE_MAPPING

__all__ = ['save', 'load']

@export
def to_hdf5(obj, hdf5_handle):
    """
    Serializes a given object to HDF5 format.

    :param obj: Object to serialize.

    :param hdf5_handle: HDF5 location where the serialized object is stored.
    :type hdf5_handle: :py:class:`h5py.File<File>` or :py:class:`h5py.Group<Group>`.
    """
    obj.to_hdf5(hdf5_handle)

@export
def from_hdf5(hdf5_handle):
    """
    Deserializes a given object from HDF5 format.

    :param hdf5_handle: HDF5 location where the serialized object is stored.
    :type hdf5_handle: :py:class:`h5py.File<File>` or :py:class:`h5py.Group<Group>`.
    """
    type_tag = hdf5_handle['type_tag'].value
    return SERIALIZE_MAPPING[type_tag].from_hdf5(hdf5_handle)

@export
def to_hdf5_file(obj, hdf5_file):
    """
    Saves the object to a file, in HDF5 format.

    :param obj: The object to be saved.

    :param hdf5_file: Path of the file.
    :type hdf5_file: str
    """
    with h5py.File(hdf5_file, 'w') as hf:
        to_hdf5(obj, hf)

save = to_hdf5_file

@export
def from_hdf5_file(hdf5_file):
    """
    Loads the object from a file in HDF5 format.

    :param hdf5_file: Path of the file.
    :type hdf5_file: str
    """
    with h5py.File(hdf5_file, 'r') as hf:
        return from_hdf5(hf)

load = from_hdf5_file
