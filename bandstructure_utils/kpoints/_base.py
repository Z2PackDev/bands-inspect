#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import abc
from .._serializable import Serializable

from fsc.export import export

@export
class KpointsBase(Serializable):
    """
    Base class for classes defining sets of k-points.
    """
    @abc.abstractproperty
    def kpoints_explicit(self):
        """
        Array containing all k-points explicitly.
        """
        pass

    def __iter__(self):
        return iter(self.kpoints_explicit)

    def __array__(self):
        return self.kpoints_explicit
