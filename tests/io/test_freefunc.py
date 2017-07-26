#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import tempfile

import pytest
import numpy as np

import bands_inspect as bi
from instances import SERIALIZABLE_INSTANCES

@pytest.mark.parametrize('instance', SERIALIZABLE_INSTANCES)
def test_save_load(instance, assert_equal):
    with tempfile.NamedTemporaryFile() as f:
        bi.io.save(instance, f.name)
        res = bi.io.load(f.name)

    assert_equal(instance, res)
