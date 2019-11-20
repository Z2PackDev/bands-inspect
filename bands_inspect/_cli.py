# -*- coding: utf-8 -*-

# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the bands-inspect CLI.
"""

import click
import numpy as np
import matplotlib.pyplot as plt

from . import io
from . import plot
from .compare import difference as _diff
from .compare import align as _align


@click.group()
def cli():
    pass


@cli.command()
@click.argument(
    'eigenval_files', nargs=2, type=click.Path(exists=True, dir_okay=False)
)
@click.option('--energy-window', nargs=2, type=float, required=False)
def difference(eigenval_files, energy_window):
    """
    Calculate the difference between two bandstructures.
    """
    ev1, ev2 = [io.load(filename) for filename in eigenval_files]

    kwargs = {}
    if energy_window:
        kwargs['weight_eigenval'] = _diff.energy_window(*energy_window)

    click.echo(_diff.calculate(ev1, ev2, **kwargs))


@cli.command()
@click.option(
    '-i',
    '--input-files',
    nargs=2,
    type=click.Path(exists=True, dir_okay=False),
    default=['eigenvals1.hdf5', 'eigenvals2.hdf5']
)
@click.option(
    '-o',
    '--output-files',
    nargs=2,
    type=click.Path(exists=False, dir_okay=False),
    default=['eigenvals1_shifted.hdf5', 'eigenvals2_shifted.hdf5']
)
@click.option('--energy-window', nargs=2, type=float, required=False)
def align(input_files, output_files, energy_window):
    """
    Align two bandstructures.
    """
    ev1, ev2 = [io.load(filename) for filename in input_files]

    kwargs = {}
    if energy_window:
        kwargs['weight_eigenval'] = _diff.energy_window(*energy_window)
    res = _align.calculate(
        ev1, ev2, symmetric_eigenval_weights=False, **kwargs
    )
    io.save(res.eigenvals1_shifted, output_files[0])
    io.save(res.eigenvals2_shifted, output_files[1])

    click.echo('Shift:      {: }'.format(res.shift))
    click.echo('Difference: {: }'.format(res.difference))


@cli.command()
@click.option(
    '--input',
    '-i',
    type=click.Path(exists=True, dir_okay=False),
    default='eigenval.hdf5',
    help='File containing the input eigenvalues (in HDF5 format).'
)
@click.option('--output', '-o', type=click.Path(dir_okay=False))
@click.argument('slice_idx', nargs=-1, type=int)
def slice_bands(input, output, slice_idx):  # pylint: disable=redefined-builtin
    """
    Modify a bandstructure by selecting/re-arranging specific bands.
    """
    eigenvals = io.load(input)
    io.save(eigenvals.slice_bands(slice_idx), output)


@cli.command()
@click.option(
    '--output',
    '-o',
    type=click.Path(exists=False, dir_okay=False),
    help='Output file for the plot.',
    default='plot.pdf'
)
@click.argument(
    'eigenvals_files',
    nargs=-1,
    type=click.Path(dir_okay=False),
    required=True
)
def plot_bands(eigenvals_files, output):
    """
    Plot one or more bandstructures which share the same set of k-points.
    """
    eigenvals_list = []
    for filename in eigenvals_files:
        eigenvals_list.append(io.load(filename))
    kpoints = eigenvals_list[0].kpoints.kpoints_explicit
    for eigenvals in eigenvals_list:
        if not np.allclose(kpoints, eigenvals.kpoints.kpoints_explicit):
            raise ValueError('K-points do not match!')
    _, axis = plt.subplots()
    for i, eigenvals in enumerate(eigenvals_list):
        plot.eigenvals(
            eigenvals,
            ax=axis,
            plot_options={
                'color': 'C{}'.format(i),
                'lw': 0.8
            }
        )
    plt.savefig(output, bbox_inches='tight')
