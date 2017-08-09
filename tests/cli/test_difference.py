#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import tempfile
import numpy as np
from click.testing import CliRunner

from bands_inspect._cli import cli

def test_cli_difference(sample):
    band_sample = sample('silicon_bands.hdf5')
    runner = CliRunner()
    with tempfile.NamedTemporaryFile() as out_file:
        run = runner.invoke(
            cli,
            [
                'difference',
                band_sample,
                band_sample,
            ],
            catch_exceptions=False
        )
    assert np.isclose(float(run.output), 0)
