#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import os
import numpy as np

import bands_inspect as bi

def test_zero_diff(sample):
    ev = bi.io.load(sample('silicon_bands.hdf5'))
    assert np.isclose(bi.compare.difference(ev, ev), 0)
