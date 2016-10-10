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

__all__ = ["H5fileAuthorityNameValidator", "H5fileDeviceNameValidator", 
           "H5fileAttributeNameValidator"]

from os import path
from taurus import isValidName, debug
from taurus.core import TaurusElementType

from taurus.core.taurusvalidator import (TaurusAttributeNameValidator, 
                                         TaurusDeviceNameValidator, 
                                         TaurusAuthorityNameValidator)
from h5filefactory import H5fileFactory

class H5fileAuthorityNameValidator(TaurusAuthorityNameValidator):
    scheme = 'h5file'
    authority = '//localhost'
    path = '(?!)'
    query = '(?!)'
    fragment = '(?!)'


class H5fileDeviceNameValidator(TaurusDeviceNameValidator): 
    scheme = 'h5file'
    authority = H5fileAuthorityNameValidator.authority
    # devname group is mandatory
    path = r'(?P<devname>(/(//+)?([A-Za-z]:/)?' \
           r'([\w.\-_]+/)*[\w.\-_]+.(h5|hdf5)))'
    query = '(?!)'
    fragment = '(?!)'

    def getNames(self, fullname, factory=None):
        """reimplemented from :class:`TaurusDeviceNameValidator`.
        """
        groups = self.getUriGroups(fullname)
        if groups is None:
            return None

        authority = groups.get('authority')
        if authority is None:
            f_or_fklass = factory or H5fileFactory
            groups['authority'] = f_or_fklass.DEFAULT_AUTHORITY

        filename = groups.get('devname').rsplit('/', 1)[1]
        groups['devname'] = path.realpath(groups.get('devname'))
        complete = '%(scheme)s:%(authority)s%(devname)s' % groups
        normal = '%(devname)s' % groups
        short = filename

        return complete, normal, short
 

class H5fileAttributeNameValidator(TaurusAttributeNameValidator):
    scheme = 'h5file'
    authority = H5fileAuthorityNameValidator.authority
    path = r'%s::(?P<attrname>(([\w.\-_]+/)*[\w.\-_]+))' %\
           H5fileDeviceNameValidator.path
    query = '(?!)'
    fragment = '(?P<cfgkey>[^# ]*)'

    def getNames(self, fullname, factory=None, fragment=False):
        """reimplemented from :class:`TaurusAttributeNameValidator`.
        """
        groups = self.getUriGroups(fullname)
        if groups is None:
            return None

        authority = groups.get('authority')
        if authority is None:
            f_or_fklass = factory or H5fileFactory
            groups['authority'] = f_or_fklass.DEFAULT_AUTHORITY

        lastelem = groups.get('attrname').rsplit('/', 1)[1]
        complete = '%(scheme)s:%(authority)s%(devname)s::%(attrname)s' % groups
        normal = '%(devname)s::%(attrname)s' % groups
        short = lastelem

        if fragment:
            key = groups.get('fragment', None)
            return complete, normal, short, key

        return complete, normal, short
