#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import numpy as np

def difference(
        eigenvals1, eigenvals2,
        *,
        avg_per_band=np.average,
        avg_all_bands=np.average,
        weight_energy=None,
        weight_band=None,
        weight_kpoint=None
    ):
    for (k1, e1), (k2, e2) in zip(zip(*eigenvals1), zip(*eigenvals2)):
        print(k1, k2)
        print(e1, e2)
