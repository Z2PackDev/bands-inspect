#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import tempfile

import pytest
import numpy as np

from kpoints_instances import KPOINTS_INSTANCES

@pytest.mark.parametrize('kpoints', KPOINTS_INSTANCES)
def test_save_load(kpoints):
    with tempfile.NamedTemporaryFile() as f:
        kpoints.to_hdf5_file(f.name)
        res = kpoints.from_hdf5_file(f.name)

    np.testing.assert_equal(res.kpoints_explicit, kpoints.kpoints_explicit)
