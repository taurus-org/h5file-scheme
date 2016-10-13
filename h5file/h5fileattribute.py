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

__all__ = ["H5fileAttribute"]

import h5py
import numpy as np

from taurus.core.taurusattribute import TaurusAttribute
from taurus.core.taurusexception import TaurusException
from taurus.core.taurusbasetypes import (DataType,
                                         TaurusAttrValue,
                                         TaurusTimeVal,
                                         DataFormat,
                                         TaurusEventType,
                                         SubscriptionState)
from taurus.core.taurushelper import Manager

from taurus.external.pint import Quantity

class H5fileAttribute(TaurusAttribute):
    '''
    A :class:`TaurusAttribute` that gives access to an H5file Process Variable.
    
    .. seealso:: :mod:`taurus.core.h5file` 
    
    .. warning:: In most cases this class should not be instantiated directly.
                 Instead it should be done via the :meth:`H5fileFactory.getAttribute`
    '''

    # helper class property that stores a reference to the corresponding factory
    _factory = None
    _scheme = 'h5file'

    # h5py uses numpy types
    hdfdtype2taurusdtype = {'b': DataType.Boolean,
                            'i': DataType.Integer,
                            'f': DataType.Float,
                            's': DataType.String
                            }

    def __init__(self, name, parent, **kwargs):
        self.call__init__(TaurusAttribute, name, parent, **kwargs)
        v = self.getNameValidator()
        urigroups = v.getUriGroups(name)
        self._attr_list = urigroups.get("attrname").split('/')
        self._value = TaurusAttrValue()
        self._label = self.getSimpleName()
        self.__subscription_state = SubscriptionState.Unsubscribed

        wantpolling = not self.isUsingEvents()
        haspolling = self.isPollingEnabled()
        if wantpolling:
            self._activatePolling()
        elif haspolling and not wantpolling:
            self.disablePolling()

    def eventReceived(self, evt_src, evt_type, evt_value):
        try:
            v = evt_value.rvalue
        except AttributeError:
            self.trace('Ignoring event from %s' % repr(evt_src))
            return
        # update the corresponding value
        self.read()
        if self.isUsingEvents():
            self.fireEvent(evt_type, self._value)

    def __fireRegisterEvent(self, listener):
        """
        Method to fire a first change event
        :param listener:
        """
        try:
            v = self.read()
            self.fireEvent(TaurusEventType.Change, v, listener)
        except:
            self.fireEvent(TaurusEventType.Error, None, listener)

    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # Necessary to overwrite
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    def isNumeric(self):
        return self.type in [DataType.Float, DataType.Integer]

    def isState(self):
        # TODO it is not generic
        return False

    def encode(self, value):
        # TODO Translate the given value into a hdf5 dataset
        return value

    def decode(self, attr_value):
        """
        Decode the dataset to the corresponding python attribute
        :param attr_value: hdf5 dataset
        :return:numpy array
        """
        # Set the attribute type
        hdfdtype = attr_value.dtype.kind
        self.type = self.hdfdtype2taurusdtype.get(hdfdtype)
        # HDF5 dataset to numpy array
        return np.array(attr_value)

    def write(self, value, with_read=True):
        # TODO: For the moment this scheme is read-only
        raise TaurusException('Attributes are read-only')

    def read(self, cache=True):
        if cache and self._value.rvalue is not None:
            return self._value
        dev = self.getParentObj()
        # each time we need to open and close the file, otherwise the
        # file content is not updated
        with h5py.File(dev.filename) as h5file:
            top = h5file
            for attr in self._attr_list:
                data = top.get(attr)
                if data is None:
                    msg = "Unable to open object (Object %s doesn't exist)" % attr
                    raise TaurusException(msg)
                top = data
            # we need to decode and copy the data while the file is still opened
            rvalue = self.decode(data)
        if np.issubdtype(rvalue.dtype, np.number):
            #Create a quantity is rvalue is numeric
            units = None #TODO: nexus file does not have units
            rvalue = Quantity(rvalue, units=units)
        self._value.rvalue = rvalue
        # TODO: No assume DataFormat._1D
        self.data_format = DataFormat._1D
        self._value.time = TaurusTimeVal.now()
        return self._value

    def poll(self):
        v = self.read(cache=False)
        self.fireEvent(TaurusEventType.Periodic, v)

    def _subscribeEvents(self):
		# TODO implement events
        pass

    def _unsubscribeEvents(self):
		# TODO implement events
        pass

    def isUsingEvents(self):
        # TODO implement events
        return False

## Just for test purpose (attr)
if __name__ == "__main__":
    import os
    from taurus.core.h5file.h5filefactory import H5fileFactory
    path2file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'test/res/sardana_scan.h5')
    attrname = 'entry259/measurement/mot76'
    fullname = "h5file:%s::%s" %(path2file, attrname)
    print fullname
    attr = H5fileFactory().getAttribute(fullname)
    print attr.read()
