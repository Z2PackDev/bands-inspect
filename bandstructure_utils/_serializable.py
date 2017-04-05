#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import abc

import h5py

class Serializable(abc.ABC):
    @abc.abstractmethod
    def to_hdf5(self, hdf5_handle):
        """
        Serializes the object to HDF5 format, attaching it to the given HDF5 handle (might be a HDF5 File or Dataset).
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_hdf5(self, hdf5_handle):
        """
        Deserializes the object stored in HDF5 format.
        """
        raise NotImplementedError

    def to_hdf5_file(self, hdf5_file):
        """
        Saves the object to a file, in HDF5 format.

        :param hdf5_file: Path of the file.
        :type hdf5_file: str
        """
        with h5py.File(hdf5_file, 'w') as hf:
            self.to_hdf5(hf)

    @classmethod
    def from_hdf5_file(cls, hdf5_file):
        """
        Loads the object from a file in HDF5 format.

        :param hdf5_file: Path of the file.
        :type hdf5_file: str
        """
        with h5py.File(hdf5_file, 'r') as hf:
            return cls.from_hdf5(hf)
