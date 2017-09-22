#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile

from bands_inspect._cli import cli

from utils import *


def test_cli_slice_bands(run_command, band_sample):
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
