# -*- coding: utf-8 -*-

# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for HDF5 serialization with the free save / load functions.
"""

import tempfile

import pytest

import bands_inspect as bi
from instances import SERIALIZABLE_INSTANCES


@pytest.mark.parametrize('instance', SERIALIZABLE_INSTANCES)
def test_save_load(instance, assert_equal):
    """
    Test that all serializable instances can be saved / loaded with the free functions.
    """
    with tempfile.NamedTemporaryFile() as f:
        bi.io.save(instance, f.name)
        res = bi.io.load(f.name)

    assert_equal(instance, res)
