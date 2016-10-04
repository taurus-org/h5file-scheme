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

__all__ = ["H5fileDevice"]

import h5py

from taurus.core.taurusdevice import TaurusDevice

class H5fileDevice(TaurusDevice):
    '''
    H5file device object. 
    '''
    
    # helper class property that stores a reference to the corresponding factory
    _factory = None
    _scheme = 'h5file'
    _description = "A H5file Device"

    def __init__(self, name, **kw):
        self.call__init__(TaurusDevice, name, **kw)
        v = self.getNameValidator()
        urigroups = v.getUriGroups(name)
        self.filename = urigroups.get("devname")

    def getFileDescriptor(self, mode='r'):
        '''
        Get a h5py file descriptor.
        :param mode: It is the open file mode
        :return: `h5py.File` object
        '''
        # TODO Add possibility to manage persistence of the fd
        return h5py.File(self.filename, mode)
