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

import weakref

from taurus.core.taurusbasetypes import TaurusElementType
from h5fileattribute import H5fileAttribute
from h5fileauthority import H5fileAuthority
from h5filedevice import H5fileDevice
from taurus.core.taurusexception import TaurusException
from taurus.core.util.log import Logger
from taurus.core.util.singleton import Singleton
from taurus.core.taurusfactory import TaurusFactory
from taurus.core.tauruspollingtimer import TaurusPollingTimer

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
        self.call__init__(Logger, name)
        self.call__init__(TaurusFactory)
        self._attrs = weakref.WeakValueDictionary()
        self._devs = weakref.WeakValueDictionary()
        self._auth = None
        self.scheme = "h5file"

    # TODO: move it to the base class
    # TODO: to be 100 % agnostic, it should not assume the parent-child relation
    def getAuthority(self, auth_name=None):
        """Obtain the H5fileDatabase object.
        :return: (H5fileAuthority)
        """
        if auth_name is None:
            auth_name = '{0}:{1}'.format(self.schemes, self.DEFAULT_AUTHORITY)

        v = self.getAuthorityNameValidator()
        if not v.isValid(auth_name):
            raise TaurusException("Invalid Hdf5 authority name %s" % auth_name)

        # TODO: factory should store a cache of authorities
        if self._auth is None:
            self._auth = H5fileAuthority(auth_name)

        return self._auth

    # TODO: move it to the base class
    # TODO: to be 100 % agnostic, it should not assume the parent-child relation
    def getDevice(self, dev_name):
        """Obtain the object corresponding to the given device name. If the 
        corresponding device already exists, the existing instance is returned. 
        Otherwise a new instance is stored and returned.
           
        :param dev_name: (str) the device name string. See
                         :mod:`taurus.core.h5file` for valid device names
        
        :return: (H5fileDevice)
         
        @throws TaurusException if the given name is invalid.
        """
        v = self.getDeviceNameValidator()
        if not v.isValid(dev_name):
            raise TaurusException("Invalid Hdf5 device name %s" % dev_name)

        fullname, _, _ = v.getNames(dev_name)
        dev = self._devs.get(fullname)
        if dev is not None:
            return dev
        dev = H5fileDevice(fullname)
        self._devs[fullname] = dev
        return dev

    # TODO: move it to the base class
    # TODO: to be 100 % agnostic, it should not assume the parent-child relation
    def getAttribute(self, attr_name):
        """Obtain the object corresponding to the given attribute name. If the 
        corresponding attribute already exists, the existing instance is
        returned. Otherwise a new instance is stored and returned. The evaluator
        device associated to this attribute will also be created if necessary.
           
        :param attr_name: (str) the attribute name string. See
                          :mod:`taurus.core.h5file` for valid attribute 
                          names
        
        :return: (H5fileAttribute)
         
        @throws TaurusException if the given name is invalid.
        """
        v = self.getAttributeNameValidator()
        if not v.isValid(attr_name):
            raise TaurusException("Invalid Hdf5 attribute name %s" % attr_name)

        fullname, _, _ = v.getNames(attr_name)
        attr = self._attrs.get(fullname)
        if attr is not None:
            return attr

        devname = v.getUriGroups(fullname).get('devname')
        dev = self._devs.get(fullname)
        if dev is None:
            dev = self.getDevice(devname)
        attr = H5fileAttribute(name=fullname, parent=dev)
        self._attrs[fullname] = attr
        return attr

    # TODO: move it to the base class
    def addAttributeToPolling(self, attribute, period, unsubscribe_evts=False):
        """Activates the polling (client side) for the given attribute with the
           given period (seconds).

           :param attribute: (taurus.core.tango.TangoAttribute) attribute name.
           :param period: (float) polling period (in seconds)
           :param unsubscribe_evts: (bool) whether or not to unsubscribe from events
        """
        tmr = self.polling_timers.get(period, TaurusPollingTimer(period))
        self.polling_timers[period] = tmr
        tmr.addAttribute(attribute, self.isPollingEnabled())

    # TODO: move it to the base class
    def removeAttributeFromPolling(self, attribute):
        """Deactivate the polling (client side) for the given attribute. If the
           polling of the attribute was not previously enabled, nothing happens.

           :param attribute: (str) attribute name.
        """
        p = None
        for period, timer in self.polling_timers.iteritems():
            if timer.containsAttribute(attribute):
                timer.removeAttribute(attribute)
                if timer.getAttributeCount() == 0:
                    p = period
                break
        if p:
            del self.polling_timers[period]

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