#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

from .kpoints import KpointsPath
from .kpoints._path import _KpointLabel

def plot(eigenvals, *, save_file, figsize=[5, 4], **kwargs):
    fig, ax = plt.subplots(figsize=figsize)
    plot_ax(eigenvals, ax=ax, **kwargs)
    plt.savefig(save_file, bbox_inches='tight')

def plot_ax(eigenvals, *, ax, ylim=None, e_fermi=0., vortex_labels=True, energy_labels=True, plot_options={'color': 'k', 'lw': 0.5}):
    ax.plot(eigenvals.eigenvals - e_fermi, **plot_options)
    ax.set_xlim(0, len(eigenvals.eigenvals))
    if ylim is not None:
        ax.set_ylim(ylim)
    if vortex_labels and hasattr(eigenvals.kpoints, 'labels'):
        labels = _merge_labels(eigenvals.kpoints.labels)
        ax.set_xticks([l.index for l in labels])
        ax.set_xticklabels([l.label for l in labels])
    else:
        ax.set_xticks([])
    if energy_labels:
        ax.yaxis.set_tick_params(direction='out', labelsize=8)
        ax.set_ylabel(r'$E$ [eV]')
    else:
        ax.set_yticks([])

def _merge_labels(labels):
    new_labels = [labels[0]]
    for l1, l2, l3 in zip(labels, labels[1:], labels[2:]):
        if l2.index - l1.index == 1:
            continue
        elif l3.index - l2.index == 1:
            new_labels.append(_KpointLabel(
                index = l2.index + 0.5,
                label = l2.label + ' | ' + l3.label
            ))
        else:
            new_labels.append(l2)
    new_labels.append(labels[-1])
    return new_labels
