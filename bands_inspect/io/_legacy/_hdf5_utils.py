# -*- coding: utf-8 -*-

# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Helper functions for serializing objects to HDF5.
"""


def nested_list_from_hdf5(hdf5_handle):
    res = []
    for idx in sorted(hdf5_handle, key=int):
        res.append(list(hdf5_handle[idx][()]))
    return res


def dict_from_hdf5(hdf5_handle):
    res = dict()
    for key in hdf5_handle:
        res[key] = hdf5_handle[key][()]
    return res
