#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import click
from . import io, compare

@click.group()
def cli():
    pass

@cli.group(invoke_without_command=True)
@click.argument(
    'eigenval_files',
    nargs=2,
    type=click.Path(exists=True, dir_okay=False)
)
@click.pass_context
def difference(ctx, eigenval_files):
    ev1 = io.load(eigenval_files[0])
    ev2 = io.load(eigenval_files[1])
    ctx.obj = ev1, ev2
    if ctx.invoked_subcommand is None:
        click.echo(compare.difference.general(ev1, ev2))

@difference.command()
@click.argument(
    'energy_window',
    nargs=2,
    type=float
)
@click.pass_context
def energy_window(ctx, energy_window):
    ev1, ev2 = ctx.obj
    click.echo(compare.difference.energy_window(ev1, ev2, energy_window=energy_window))
