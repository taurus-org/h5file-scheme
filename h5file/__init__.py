#!/usr/bin/env python
#############################################################################
##
## This file is part of Taurus
## 
## http://taurus-scada.org
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Taurus is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Taurus is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""
HDF5 files extension for taurus core model.

This is a Taurus scheme that provides access to the contents of hdf5 files
as Taurus Attributes. It uses :mod:`h5py`.

h5py.File objects are mapped as H5fileDevices and the datasets within the file
are mapped as H5fileAttributes.

For example, to get the value of a the dataset foo/bar from the file
/path/to/myfile.h5, you should do something like::

    >>> import taurus
    >>> myattr = taurus.Attribute('h5file:/path/to/myfile.h5::foo/bar')

h5file attributes (should) work just as other Taurus attributes and can be
referred by their model name wherever a Taurus Attribute model is expected. For
example, you can launch a `TaurusForm` with a h5file attribute::

    $> taurusform h5file:/path/to/myfile.h5::foo/bar

Similarly, you can combine h5file attributes with attributes from other
schemes::

    $> taurusform 'h5file:/path/to/myfile.h5::foo/bar' \
       'tango:sys/tg_test/1/float_scalar'\
       'eval:{h5file:/path/to/myfile.h5::foo/bar}*{tango:sys/tg_test/1/ampli}'

"""

from __future__ import absolute_import

# TODO: document syntax

from .h5fileattribute import *                                                    
from .h5fileauthority import *
from .h5filedevice import *
from .h5filefactory import *
from .h5filevalidator import *

