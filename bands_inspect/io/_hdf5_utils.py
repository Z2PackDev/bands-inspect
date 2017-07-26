#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import h5py
import numpy as np

def _nested_list_to_hdf5(hdf5_handle, value, special_dtype=None):
    if special_dtype is None:
        dtype=None
    else:
        dtype = h5py.special_dtype(vlen=special_dtype)
        value = [np.array(el, dtype=object) for el in value]
    for i, element in enumerate(value):
        hdf5_handle.create_dataset(
            str(i),
            data=element,
            dtype=dtype
        )

def _nested_list_from_hdf5(hdf5_handle):
    res = []
    for idx in sorted(hdf5_handle, key=int):
        res.append(list(hdf5_handle[idx].value))
    return res

def _dict_to_hdf5(hdf5_handle, value):
    for key, val in value.items():
        hdf5_handle[key] = val

def _dict_from_hdf5(hdf5_handle):
    res = dict()
    for key in hdf5_handle:
        res[key] = hdf5_handle[key].value
    return res
