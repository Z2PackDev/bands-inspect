# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Test for the 'bands-inspect slice_bands' command.
"""

import tempfile

from utils import *  # pylint: disable=unused-wildcard-import


def test_cli_slice_bands(run_command, band_sample):  # pylint: disable=redefined-outer-name
    """
    Basic test that the slice_bands command runs without error.
    """
    with tempfile.NamedTemporaryFile() as outfile:
        run_command([
            'slice_bands',
            '-i',
            band_sample,
            '-o',
            outfile.name,
            '--',
            1,
            2,
            3,
        ])
