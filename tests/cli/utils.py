"""
Helper fixtures for running CLI tests.
"""

import pytest
from click.testing import CliRunner

from bands_inspect._cli import cli


@pytest.fixture
def run_command():
    def inner(args):
        return CliRunner().invoke(cli, args, catch_exceptions=False)

    return inner


@pytest.fixture
def band_sample(sample):
    return sample('silicon_bands.hdf5')
