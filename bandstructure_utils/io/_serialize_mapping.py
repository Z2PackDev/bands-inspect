#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from decorator import decorator

SERIALIZE_MAPPING = {}

def subscribe_serialize(type_tag):
    def inner(cls):
        SERIALIZE_MAPPING[type_tag] = cls

        @decorator
        def set_type_tag(to_hdf5_func, self, hdf5_handle):
            hdf5_handle['type_tag'] = type_tag
            return to_hdf5_func(self, hdf5_handle)

        cls.to_hdf5 = set_type_tag(cls.to_hdf5)

        @decorator
        def check_type_tag(from_hdf5_func, self, hdf5_handle):
            assert hdf5_handle['type_tag'].value == type_tag
            return from_hdf5_func(self, hdf5_handle)

        cls.from_hdf5 = classmethod(check_type_tag(cls.from_hdf5.__func__))
        return cls
    return inner
