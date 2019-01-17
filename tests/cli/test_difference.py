# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Tests for the 'bands-inspect difference' command.
"""

import numpy as np

from utils import *  # pylint: disable=unused-wildcard-import


def test_cli_difference(run_command, band_sample):  # pylint: disable=redefined-outer-name
    """
    Test the difference command on two identical bandstructures.
    """
    run = run_command([
        'difference',
        band_sample,
        band_sample,
    ])
    assert np.isclose(float(run.output), 0)


def test_cli_difference_energy_window(run_command, band_sample):  # pylint: disable=redefined-outer-name,invalid-name
    """
    Test the difference command on two identical bandstructures, with the energy-window option.
    """
    run = run_command([
        'difference',
        '--energy-window',
        -1,
        4,
        band_sample,
        band_sample,
    ])
    assert np.isclose(float(run.output), 0)
