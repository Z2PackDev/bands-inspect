#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import tempfile

import pytest
import numpy as np

from instances import SERIALIZABLE_INSTANCES


@pytest.mark.parametrize('instance', SERIALIZABLE_INSTANCES)
def test_save_load(instance, assert_equal):
    with tempfile.NamedTemporaryFile() as f:
        instance.to_hdf5_file(f.name)
        res = instance.from_hdf5_file(f.name)

    assert_equal(instance, res)
