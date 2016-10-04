#!/usr/bin/env python

#############################################################################
##
# This file is part of Taurus
##
# http://taurus-scada.org
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""Test for taurus.core.h5file.test.test_h5filevalidator..."""

__docformat__ = 'restructuredtext'


from taurus.external import unittest
from taurus.core.test import (valid, invalid, names,
                              AbstractNameValidatorTestCase)
from taurus.core.h5file.h5filevalidator import \
                                (H5fileAuthorityNameValidator,
                                 H5fileDeviceNameValidator,
                                 H5fileAttributeNameValidator)
from taurus import tauruscustomsettings


#=========================================================================
# Tests for H5file Authority name validation
#=========================================================================
@valid(name='h5file://localhost')
@invalid(name='h5file:')
@names(name='h5file://localhost',
       out=('h5file://localhost', '//localhost', 'localhost'))
class H5fileAuthValidatorTestCase(AbstractNameValidatorTestCase,
                                 unittest.TestCase):
    validator = H5fileAuthorityNameValidator

#=========================================================================
# Tests for H5file Device name validation
#=========================================================================
@valid(name='h5file://localhost/path/to/file.h5')
@valid(name='h5file:/path/to/file.h5')
@valid(name='h5file:/path-to/file.h5')
@valid(name='h5file:/path_to/file.h5')
@valid(name='h5file:/path/../to/file.h5')
@valid(name='h5file:/c:/path/to/file.h5')
@valid(name='h5file:/C:/path/TO/File.h5')
@valid(name='h5file:/../file.hdf5')
@valid(name='h5file:/file.h5')
@valid(name='h5file:/_._-/file.h5')
@valid(name='h5file:/path-to/fi-le.h5')
@valid(name='h5file:/path_to/fi_le.h5')
@valid(name='h5file:/path-to/f.i.l.e..h5')
@valid(name='h5file:/path_to/f_i-l.e.h5')
@valid(name='h5file:///path/file.h5')
@invalid(name='h5file:/path/to/file.h5/') # Has a extra final "/"
@invalid(name='h5file:/path/to/file.h5::') # Has a extra final "::"
@invalid(name='h5file:/path/to/file.h5::Foo') # It is an attr URI
@invalid(name='h5file://path/to/file.h5') # Path can not start with "//"
@invalid(name='h5file:path/to/') # Missing first "/"
@invalid(name='h5file:../file.hdf5') # Missing first "/
@invalid(name='h5file:/path/to/file') # Missing file extension
@invalid(name='h5file:/path/to/file.f5') # Invalid file extension
@invalid(name='h5file:/1:/path/to/file.h5') # Windows unit must be a letter
                                          # TODO: We could accept them
@invalid(name='h5file:/path-to/fi le.h5') # White spaces are not accepted
@invalid(name='h5file:/pa th/my-file.h5') # White spaces are not accepted
@names(name='h5file:/path/to/file.h5',
       out=('h5file://localhost/path/to/file.h5', '/path/to/file.h5',
            'file.h5'))
@names(name='h5file:/file.h5',
       out=('h5file://localhost/file.h5', '/file.h5',
            'file.h5'))
@names(name='h5file:/a/../c/file.h5',
       out=('h5file://localhost/c/file.h5', '/c/file.h5',
            'file.h5'))
@names(name='h5file:/../file.h5',
       out=('h5file://localhost/file.h5', '/file.h5',
            'file.h5'))
@names(name='h5file:/foo/./file.h5',
       out=('h5file://localhost/foo/file.h5', '/foo/file.h5',
            'file.h5'))
@names(name='h5file:/foo/.../file.h5',
       out=('h5file://localhost/foo/.../file.h5', '/foo/.../file.h5',
            'file.h5'))
class H5fileDevValidatorTestCase(AbstractNameValidatorTestCase,
                                 unittest.TestCase):
    validator = H5fileDeviceNameValidator

#=========================================================================
# Tests for H5file Attribute name validation
#=========================================================================
@valid(name='h5file://localhost/path/to/file.h5::group/dataset/attribute')
@valid(name='h5file://localhost/path/to/file.h5::group/subgroup/subgroup')
@valid(name='h5file://localhost/path/to/file.h5::group/dataset')
@valid(name='h5file://localhost/path/to/file.h5::group')
@valid(name='h5file:/path/to/file.h5::group/dataset/attribute')
@valid(name='h5file:/path/to/file.h5::group/dataset')
@valid(name='h5file:/path/to/file.h5::group')
@valid(name='h5file:/file.h5::group')
@valid(name='h5file:/file.h5::_group')
@valid(name='h5file:/file.h5::GRouP')
@valid(name='h5file:/file.h5::gr_up')
@valid(name='h5file:/file.h5::Foo')
@valid(name='h5file:/file.h5::Foo-1')
@valid(name='h5file:/file.h5::Foo_1/bar-2')
@valid(name='h5file:/c:/path/to/file.h5::group/dataset/attribute')
@valid(name='h5file:/c:/path/to/file.h5::group/dataset')
@valid(name='h5file:/c:/path/to/file.h5::group')
@invalid(name='h5file://localhost/path/to/file.h5::') # empty attribute
@invalid(name='h5file://localhost/path/to/file.h5:://') # Invalid group "//"
@invalid(name='h5file:/path/to/file.h5::/Foo') # Group can not start with "/"
@invalid(name='h5file:/path/to/file.h5::Foo 1') # White space are not valid
@invalid(name='h5file:/path/to/file.h5:foo/bar') # Attr must be separate by "::"
@names(name='h5file://localhost/path/to/file.h5::group/dataset/attribute',
       out=('h5file://localhost/path/to/file.h5::group/dataset/attribute',
            '/path/to/file.h5::group/dataset/attribute', 'attribute'))
@names(name='h5file:/path/to/file.hdf5::Foo/Bar',
       out=('h5file://localhost/path/to/file.hdf5::Foo/Bar',
            '/path/to/file.hdf5::Foo/Bar', 'Bar'))
class h5fileAttrValidatorTestCase(AbstractNameValidatorTestCase,
                                 unittest.TestCase):
    validator = H5fileAttributeNameValidator

