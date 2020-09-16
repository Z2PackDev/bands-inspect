# -*- coding: utf-8 -*-

# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Configuration file for the pytest tests.
"""

import os
import json

import pytest
import numpy as np

import bands_inspect as bi

import parameters  # pylint: disable=wrong-import-order

#--------------------------FIXTURES-------------------------------------#


@pytest.fixture
def test_name(request):
    """Returns module_name.function_name for a given test"""
    return request.module.__name__ + '/' + request._parent_request._pyfuncitem.name  # pylint: disable=protected-access


@pytest.fixture
def compare_data(request, test_name, scope="session"):  # pylint: disable=unused-argument,redefined-outer-name
    """Returns a function which either saves some data to a file or (if that file exists already) compares it to pre-existing data using a given comparison function."""
    def inner(compare_fct, data, tag=None):
        full_name = test_name + (tag or '')

        # get rid of json-specific quirks
        # store as string because I cannot add the decoder to the pytest cache
        data_str = json.dumps(data)
        data = json.loads(data_str)
        val = json.loads(request.config.cache.get(full_name, 'null'))

        if val is None:
            request.config.cache.set(full_name, data_str)
            raise ValueError('Reference data does not exist.')
        assert compare_fct(val, data)

    return inner


@pytest.fixture
def compare_equal(compare_data):  # pylint: disable=redefined-outer-name
    """
    Returns a function which checks that a given data is equal to the stored reference.
    """
    return lambda data, tag=None: compare_data(lambda x, y: x == y, data, tag)


@pytest.fixture
def assert_equal():
    """
    Returns a function which checks that two bands-inspect object instances are equal.
    """
    def inner(obj1, obj2):
        if isinstance(obj1, bi.kpoints.KpointsBase):
            np.testing.assert_equal(
                obj1.kpoints_explicit, obj2.kpoints_explicit
            )
        elif isinstance(obj1, bi.eigenvals.EigenvalsData):
            np.testing.assert_equal(
                obj1.kpoints.kpoints_explicit, obj2.kpoints.kpoints_explicit
            )
            np.testing.assert_equal(obj1.eigenvals, obj2.eigenvals)
        else:
            raise ValueError("Unknown type {}".format(type(obj1)))

    return inner


@pytest.fixture
def sample():
    """
    Returns the absolute path of the sample with a given name.
    """
    def inner(name):
        return os.path.join(parameters.SAMPLES_DIR, name)

    return inner
