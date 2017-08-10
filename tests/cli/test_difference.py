#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import numpy as np
from click.testing import CliRunner

from bands_inspect._cli import cli

@pytest.fixture
def run_command():
    def inner(args):
        return CliRunner().invoke(
            cli,
            args,
            catch_exceptions=False
        )
    return inner

@pytest.fixture
def band_sample(sample):
    return sample('silicon_bands.hdf5')

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

# def test_cli_select_bands(run_command, band_sample):
#     run = run_command([
#         'difference',
#         band_sample,
#         band_sample,
#         'select_bands',
#         '--',
#         1, 2, 3
#     ])
#     assert np.isclose(float(run.output), 0)
