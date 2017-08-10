#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import numpy as np
from click.testing import CliRunner

from bands_inspect._cli import cli

from utils import * 

def test_cli_difference(run_command, band_sample):
    run = run_command([
        'difference',
        band_sample,
        band_sample,
    ])
    assert np.isclose(float(run.output), 0)

def test_cli_difference_energy_bands(run_command, band_sample):
    run = run_command([
        'difference',
        '--energy-window',
        -1, 4,
        band_sample, band_sample,
    ])
    assert np.isclose(float(run.output), 0)
