# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for serialization with the member functions.
"""

import tempfile

import pytest

from instances import (  # pylint: disable=import-error,useless-suppression
    SERIALIZABLE_INSTANCES,
)


@pytest.mark.parametrize("instance", SERIALIZABLE_INSTANCES)
def test_save_load(instance, assert_equal):
    """
    Test that all serializable instances can be saved / loaded with their member functions.
    """
    with tempfile.NamedTemporaryFile() as f:
        instance.to_hdf5_file(f.name)
        res = instance.from_hdf5_file(f.name)

    assert_equal(instance, res)
