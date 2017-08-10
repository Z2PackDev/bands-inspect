#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import click
from . import io
from .compare import difference as _diff

@click.group()
def cli():
    pass

@cli.command()
@click.argument(
    'eigenval_files',
    nargs=2,
    type=click.Path(exists=True, dir_okay=False)
)
@click.option(
    '--energy-window',
    nargs=2,
    type=float,
    required=False
)
def difference(eigenval_files, energy_window):
    ev1, ev2 = [io.load(filename) for filename in eigenval_files]

    kwargs = {}
    if energy_window:
        kwargs['weight_eigenval'] = _diff.energy_window(*energy_window)

    click.echo(_diff.calculate(ev1, ev2, **kwargs))

# @cli.group()
# def ():
