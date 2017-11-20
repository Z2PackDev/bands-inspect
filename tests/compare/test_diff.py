"""
Tests for the functions that calculat the difference between bandstructures.
"""

import numpy as np
import pytest

import bands_inspect as bi
from bands_inspect.compare import difference as diff


@pytest.fixture
def simple_eigenvals():
    """
    Fixture that creates two different simple bandstructures.
    """
    ev1 = bi.eigenvals.EigenvalsData(
        kpoints=[[0.1], [0.2]], eigenvals=[[1, 2], [3, 4]]
    )
    ev2 = bi.eigenvals.EigenvalsData(
        kpoints=[[0.1], [0.2]], eigenvals=[[1, 2], [3, 5]]
    )
    return ev1, ev2


def test_zero_diff(sample):
    eigenvals = bi.io.load(sample('silicon_bands.hdf5'))
    assert np.isclose(diff.calculate(eigenvals, eigenvals), 0)


def test_nonzero_diff(simple_eigenvals):  # pylint: disable=redefined-outer-name
    assert np.isclose(diff.calculate(*simple_eigenvals), 1 / 4)


def test_energy_window_1(simple_eigenvals):  # pylint: disable=redefined-outer-name
    assert np.isclose(
        diff.calculate(
            *simple_eigenvals, weight_eigenval=diff.energy_window(0, 3.5)
        ), 0
    )


def test_energy_window_2(simple_eigenvals):  # pylint: disable=redefined-outer-name
    assert np.isclose(
        diff.calculate(
            *simple_eigenvals, weight_eigenval=diff.energy_window(3.5, 5)
        ), 1
    )


def test_energy_window_3(simple_eigenvals):  # pylint: disable=redefined-outer-name
    assert np.isclose(
        diff.calculate(
            *simple_eigenvals, weight_eigenval=diff.energy_window(2.9, 4.1)
        ), 1 / 3
    )


def test_energy_window_4(simple_eigenvals):  # pylint: disable=redefined-outer-name
    assert np.isclose(
        diff.calculate(
            *simple_eigenvals,
            symmetric_eigenval_weights=False,
            weight_eigenval=diff.energy_window(2.9, 4.1)
        ), 1 / 2
    )
