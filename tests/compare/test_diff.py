#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os
import numpy as np

import bandstructure_utils as bs

def test_zero_diff(sample):
    ev = bs.io.load(sample('silicon_bands.hdf5'))
    assert np.isclose(bs.compare.difference(ev, ev), 0)
