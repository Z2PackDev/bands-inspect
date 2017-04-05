#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

import abc
from .._serializable import Serializable

from fsc.export import export

class KpointsBase(Serializable):
    @abc.abstractproperty
    def kpoints_explicit(self):
        """
        Array containing all k-points explicitly.
        """
        pass
