#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import tempfile

import pytest
import numpy as np

import bandstructure_utils as bs
from instances import SERIALIZABLE_INSTANCES

@pytest.mark.parametrize('instance', SERIALIZABLE_INSTANCES)
def test_save_load(instance, assert_equal):
    with tempfile.NamedTemporaryFile() as f:
        bs.io.save(instance, f.name)
        res = bs.io.load(f.name)

    assert_equal(instance, res)
