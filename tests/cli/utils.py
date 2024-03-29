# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <mail@greschd.ch>
"""
Helper fixtures for running CLI tests.
"""

import pytest
from click.testing import CliRunner

from bands_inspect._cli import cli


@pytest.fixture
def run_command():
    """
    Invoke the CLI with the given arguments.
    """

    def inner(args):
        return CliRunner().invoke(cli, args, catch_exceptions=False)

    return inner


@pytest.fixture
def band_sample(sample):
    """
    Fixture which returns a bands sample file.
    """
    return sample("silicon_bands.hdf5")
