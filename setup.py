#!/usr/bin/env python

##############################################################################
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
##############################################################################

from setuptools import setup, find_packages

version = '0.0.2'
description = 'h5file Taurus scheme'
long_description = ''' h5file is the Taurus scheme for accessing hdf5 files.
This first implementation offers a read-only scheme with basic interface to
access hdf5 files.'''
license = 'LGPL'
platforms = ['Linux', 'Windows']


authors = 'ctgensoft'
email = 'ctgensoft@cells.es'
url = 'http://www.taurus-scada.org/en/stable/devel/core_tutorial.html'

install_requires = ['taurus>=4.0.1',
                    'h5py']

entry_points = {
    "taurus.core.schemes": ["h5file = h5file",],
}


setup(name='h5file',
      version=version,
      description=description,
      long_description=long_description,
      author=authors,
      maintainer=authors,
      maintainer_email=email,
      url=url,
      platforms=platforms,
      license=license,
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      test_suite='h5file.test.testsuite.get_suite',
      entry_points=entry_points,
      )
