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

from taurus.external.pint import Quantity, UndefinedUnitError

class H5fileAttribute(TaurusAttribute):
    '''
    A :class:`TaurusAttribute` that gives access to an H5file Process Variable.
    
    .. seealso:: :mod:`taurus.core.h5file` 
    
    .. warning:: In most cases this class should not be instantiated directly.
                 Instead it should be done via the :meth:`H5fileFactory.getAttribute`
    '''

    _scheme = 'h5file'

    # h5py uses numpy types
    hdfdtype2taurusdtype = {'b': DataType.Boolean,
                            'i': DataType.Integer,
                            'f': DataType.Float,
                            's': DataType.String
                            }

    def __init__(self, name, parent, **kwargs):
        TaurusAttribute.__init__(self, name, parent, **kwargs)
        v = self.getNameValidator()
        urigroups = v.getUriGroups(name)
        # TODO: not necessary - execute a readout at once
        # but store the dsat_path here for the future readouts
        self._attr_name = urigroups.get("attrname")
        self._last_value = None

        wantpolling = not self.isUsingEvents()
        haspolling = self.isPollingEnabled()
        if wantpolling:
            self._activatePolling()
        elif haspolling and not wantpolling:
            self.disablePolling()


    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # Necessary to overwrite
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    def isNumeric(self):
        return self.type in [DataType.Float, DataType.Integer]

    # TODO: this is tango centric
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
        :return:taurus valid type
        """
        # Transform hdf5 attribute to numpy array
        attr_value_np = np.array(attr_value)
        # TODO: extract scalars from hdf5 attribute
        # attr_value = attr_value_np[0]

        # get the attribute type
        hdfdtype = attr_value_np.dtype.kind
        self.type = self.hdfdtype2taurusdtype.get(hdfdtype)

        dimension = len(np.shape(attr_value_np))
        if dimension == 0:
            self.data_format = DataFormat._0D
        elif dimension == 1:
            self.data_format = DataFormat._1D
        elif dimension == 2:
            self.data_format = DataFormat._2D

        if self.isNumeric():
            # get units hdf5 attribute if it exist
            units = attr_value.attrs.get("units")
            # numeric attributes must be Quantities
            try:
                value = Quantity(attr_value_np, units=units)
            except UndefinedUnitError:
                value = Quantity(attr_value_np, units="dimensionless")
        elif self.type is DataType.String:
            value = attr_value_np.tolist()
        return value

    def write(self, value, with_read=True):
        # TODO: For the moment this scheme is read-only
        raise TaurusException('Attributes are read-only')

    def isWritable(self, cache=True):
        # TODO: This method is need if the scheme is writable
        return self.writable

    def read(self, cache=True):
        if cache and self._last_valuevalue is not None:
            return self._last_value
        dev = self.getParentObj()
        # each time we need to open and close the file, otherwise the
        # file content is not updated
        with h5py.File(dev.filename) as h5file:
            data = h5file.get(self._attr_name)
            if data is None:
                msg = "Unable to open object (Object %s doesn't exist)" % attr
                raise TaurusException(msg)
            # we need to decode and copy the data while the file is still opened
            rvalue = self.decode(data)
        value = TaurusAttrValue()
        value.rvalue = rvalue
        value.time = TaurusTimeVal.now()
        self._last_value = value
        return value

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
