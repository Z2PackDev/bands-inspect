#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from fsc.export import export

from ._serialize_mapping import SERIALIZE_MAPPING

@export
def to_hdf5(obj, hdf5_handle):
    obj.to_hdf5(hdf5_handle)

@export
def from_hdf5(hdf5_handle):
    type_tag = hdf5_handle['type_tag'].value
    return SERIALIZE_MAPPING[type_tag].from_hdf5(hdf5_handle)
