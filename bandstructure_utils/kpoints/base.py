#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import abc
import h5py

class KpointsBase(abc.ABC):
    @abc.abstractproperty
    def kpoints_explicit(self):
        """
        Array containing all k-points explicitly.
        """
        pass

    @abc.abstractmethod
    def to_hdf5(self, hdf5_handle):
        """
        Serializes the object to HDF5 format, attaching it to the given HDF5 handle (might be a HDF5 File or Dataset).
        """
        pass

    @classmethod
    @abc.abstractmethod
    def from_hdf5(self, hdf5_handle):
        """
        Deserializes the object stored in HDF5 format.
        """
        pass

    def to_hdf5_file(self, hdf5_file):
        with h5py.File(hdf5_file, 'w') as hf:
            self.to_hdf5(hf)

    @classmethod
    def from_hdf5_file(cls, hdf5_file):
        with h5py.File(hdf5_file, 'r') as hf:
            return cls.from_hdf5(hf)
