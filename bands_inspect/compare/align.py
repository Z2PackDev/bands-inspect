# -*- coding: utf-8 -*-

# (c) 2019, Microsoft Research
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines a function to align two bandstructures in such a way
that their difference is minimized.
"""

from collections import namedtuple

import numpy as np
from scipy.optimize import minimize

from fsc.export import export

from .difference import calculate as calculate_diff

AlignResult = namedtuple(
    'AlignResult',
    ['shift', 'eigenvals1_shifted', 'eigenvals2_shifted', 'difference']
)


@export
def calculate(eigenvals1, eigenvals2, *, symmetric_shift=False, **kwargs):
    """
    Shift the two sets of eigenvalues such that their difference is minimized.

    :param eigenvals1: The first set of eigenvalues.
    :type eigenvals1: EigenvalsData

    :param eigenvals2: The second set of eigenvalues.
    :type eigenvals2: EigenvalsData

    :param symmetric_shift: If `True`, the two sets of eigenvalues are shifted by
        equal and opposite values. Otherwise, only the second set of eigenvalues
        is shifted.
    :type symmetric_shift: bool

    :param kwargs: Keyword arguments passed on to :func:`.difference.calculate`.
    :type kwargs: dict
    """
    def _do_shift(shift_delta):
        if symmetric_shift:
            return (
                eigenvals1.shift(-shift_delta / 2),
                eigenvals2.shift(shift_delta / 2)
            )
        return eigenvals1, eigenvals2.shift(shift_delta)

    def opt_func(delta):
        shift_delta, = delta
        ev1, ev2 = _do_shift(shift_delta=shift_delta)
        return calculate_diff(eigenvals1=ev1, eigenvals2=ev2, **kwargs)

    res = minimize(fun=opt_func, x0=np.array([0]))
    shift, = res.x
    ev1, ev2 = _do_shift(shift_delta=shift)
    difference = res.fun
    return AlignResult(
        shift=shift,
        eigenvals1_shifted=ev1,
        eigenvals2_shifted=ev2,
        difference=difference
    )
