#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

from .kpoints import KpointsPath

def plot(eigenvals, *, special_labels={}):
    kpoints = eigenvals.kpoints
