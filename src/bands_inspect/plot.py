# (c) 2017-2019, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <mail@greschd.ch>
"""
Defines functions to plot bandstructures.
"""

from types import MappingProxyType

import decorator

from .kpoints._path import _KpointLabel


@decorator.decorator
def _plot(  # pylint: disable=missing-docstring,invalid-name,inconsistent-return-statements
    func, data, *, ax=None, **kwargs
):
    import matplotlib.pyplot as plt  # pylint: disable=import-outside-toplevel

    if ax is None:
        return_fig = True
        fig, ax = plt.subplots()  # pylint: disable=invalid-name
    else:
        return_fig = False

    func(data, ax=ax, **kwargs)

    if return_fig:
        return fig


@_plot
def eigenvals(
    eigenvals,  # pylint:disable=redefined-outer-name
    *,
    ax=None,  # pylint:disable=invalid-name
    ylim=None,
    e_fermi=0.0,
    vertex_labels=True,
    energy_labels=True,
    plot_options=MappingProxyType({"color": "C0", "lw": 0.8})
):
    """
    Plot the bandstructure of a given :class:`.EigenvalsData` object.
    """
    ax.plot(eigenvals.eigenvals - e_fermi, **plot_options)
    ax.set_xlim(0, len(eigenvals.eigenvals) - 1)
    if ylim is not None:
        ax.set_ylim(ylim)
    if vertex_labels and hasattr(eigenvals.kpoints, "labels"):
        labels = _merge_labels(eigenvals.kpoints.labels)
        ax.set_xticks([l.index for l in labels])
        ax.set_xticklabels([l.label for l in labels])
        ax.xaxis.grid(True)
    else:
        ax.set_xticks([])
    if energy_labels:
        ax.yaxis.set_tick_params(direction="out", labelsize=8)
        ax.set_ylabel(r"$E$ [eV]")
    else:
        ax.set_yticks([])


def _merge_labels(labels):
    """
    Merge labels of neighbouring k-points, separating them by a ' | '.
    """
    new_labels = [labels[0]]
    for left_label, middle_label, right_label in zip(labels, labels[1:], labels[2:]):
        if middle_label.index - left_label.index == 1:
            continue
        if right_label.index - middle_label.index == 1:
            new_labels.append(
                _KpointLabel(
                    index=middle_label.index + 0.5,
                    label=middle_label.label + " | " + right_label.label,
                )
            )
        else:
            new_labels.append(middle_label)
    new_labels.append(labels[-1])
    return new_labels
