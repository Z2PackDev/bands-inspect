"""
Defines the bands-inspect CLI.
"""

import click
from . import io
from .compare import difference as _diff


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
