"""
Tests of the 'align' feature.
"""

import numpy as np
import pytest

import bands_inspect as bi
from bands_inspect.compare import align


def test_noshift_nodiff():
    """
    Test aligning a bandstructure with itself.
    """
    ev1 = bi.eigenvals.EigenvalsData(kpoints=[[0.1], [0.2]], eigenvals=[[1, 2], [3, 5]])
    ev2 = ev1
    res = align.calculate(ev1, ev2)
    assert res.shift == 0
    assert res.difference == 0


def test_shift_nodiff():
    """
    Test aligning two bandstructures which match perfectly.
    """
    ev1 = bi.eigenvals.EigenvalsData(kpoints=[[0.1], [0.2]], eigenvals=[[1, 2], [3, 5]])
    ev2 = bi.eigenvals.EigenvalsData(
        kpoints=[[0.1], [0.2]], eigenvals=[[1.2, 2.2], [3.2, 5.2]]
    )
    res = align.calculate(ev1, ev2)
    assert np.isclose(res.shift, -0.2)
    assert np.isclose(res.difference, 0.0)


def test_noshift_diff():
    """
    Test aligning two bandstructures have zero total shift, but a nonzero difference.
    """
    ev1 = bi.eigenvals.EigenvalsData(kpoints=[[0.1], [0.2]], eigenvals=[[1, 2], [3, 5]])
    ev2 = bi.eigenvals.EigenvalsData(
        kpoints=[[0.1], [0.2]], eigenvals=[[1.2, 1.8], [3.3, 4.7]]
    )
    res = align.calculate(ev1, ev2)
    assert np.isclose(res.shift, 0)
    assert np.isclose(res.difference, bi.compare.difference.calculate(ev1, ev2))


def test_kpoints_check():
    """
    Test that two band structures with unequal k-points cannot be aligned.
    """
    ev1 = bi.eigenvals.EigenvalsData(kpoints=[[0.1], [0.2]], eigenvals=[[1, 2], [3, 5]])
    ev2 = bi.eigenvals.EigenvalsData(
        kpoints=[[0.1], [0.3]], eigenvals=[[1.2, 1.8], [3.3, 4.7]]
    )
    with pytest.raises(ValueError):
        align.calculate(ev1, ev2)
