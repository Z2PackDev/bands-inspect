#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os
import numpy as np
import pytest

import bands_inspect as bi

@pytest.fixture
def simple_eigenvals():
    ev1 = bi.eigenvals.EigenvalsData(
        kpoints=[[0.1], [0.2]],
        eigenvals=[[1, 2], [3, 4]]
    )
    ev2 = bi.eigenvals.EigenvalsData(
        kpoints=[[0.1], [0.2]],
        eigenvals=[[1, 2], [3, 5]]
    )
    return ev1, ev2

def test_zero_diff(sample):
    ev = bi.io.load(sample('silicon_bands.hdf5'))
    assert np.isclose(bi.compare.difference(ev, ev), 0)

def test_nonzero_diff(simple_eigenvals):
    assert np.isclose(bi.compare.difference(*simple_eigenvals), 1 / 4)

def test_energy_window_1(simple_eigenvals):
    assert np.isclose(
        bi.compare.difference_energy_window(
            *simple_eigenvals,
            energy_window=(0, 3.5)
        ),
        0
    )

def test_energy_window_2(simple_eigenvals):
    assert np.isclose(
        bi.compare.difference_energy_window(
            *simple_eigenvals,
            energy_window=(3.5, 5)
        ),
        1
    )

def test_energy_window_3(simple_eigenvals):
    assert np.isclose(
        bi.compare.difference_energy_window(
            *simple_eigenvals,
            energy_window=(2.9, 4.1)
        ),
        1 / 3
    )

def test_energy_window_4(simple_eigenvals):
    assert np.isclose(
        bi.compare.difference_energy_window(
            *simple_eigenvals,
            symmetric_eigenval_weights=False,
            energy_window=(2.9, 4.1)
        ),
        1 / 2
    )
