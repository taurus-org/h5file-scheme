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

__all__ = ['H5fileFactory']

try:
    import h5py
except ImportError:
    # note that if PyTango is not installed the factory will not be available
    from taurus.core.util.log import debug
    msg = 'cannot import h5py module. ' + \
          'Taurus will not support the "h5file" scheme'
    debug(msg)
    raise

from taurus.core.taurusbasetypes import TaurusElementType
from h5fileattribute import H5fileAttribute
from h5fileauthority import H5fileAuthority
from h5filedevice import H5fileDevice
from taurus.core.util.log import Logger
from taurus.core.util.singleton import Singleton
from taurus.core.taurusfactory import TaurusFactory

class H5fileFactory(Singleton, TaurusFactory, Logger):
    """
    A Singleton class that provides H5file related objects.
    """
    schemes = ("h5file",)
    elementTypesMap = {TaurusElementType.Authority: H5fileAuthority,
                       TaurusElementType.Device: H5fileDevice,
                       TaurusElementType.Attribute: H5fileAttribute
                       }

    DEFAULT_AUTHORITY = '//localhost'

    # TODO this scheme is case-insensitive on Windows by default the schemes are
    # considered case-sensitive

    def __init__(self):
        """ Initialization. Nothing to be done here for now."""
        pass

    def init(self, *args, **kwargs):
        """Singleton instance initialization."""
        name = self.__class__.__name__
        Logger.__init__(self, name)
        TaurusFactory.__init__(self)
        self.scheme = "h5file"

    def getAuthorityNameValidator(self):
        """Return H5fileDatabaseNameValidator"""
        import h5filevalidator
        return h5filevalidator.H5fileAuthorityNameValidator()

    def getDeviceNameValidator(self):
        """Return H5fileDeviceNameValidator"""
        import h5filevalidator
        return h5filevalidator.H5fileDeviceNameValidator()

    def getAttributeNameValidator(self):
        """Return H5fileAttributeNameValidator"""
        import h5filevalidator
        return h5filevalidator.H5fileAttributeNameValidator()


## Just for test purpose
if __name__ == "__main__":
    import taurus
    f = taurus.Factory('h5file')
    f2 = H5fileFactory()
    print f2.scheme