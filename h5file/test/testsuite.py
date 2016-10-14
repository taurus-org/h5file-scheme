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

from taurus.external import unittest

def get_suite():
    # use the default shared TestLoader instance
    test_loader = unittest.defaultTestLoader
    # use the basic test runner that outputs to sys.stderr
    test_runner = unittest.TextTestRunner()
    # automatically discover all tests in the current dir of the form test*.py
    # NOTE: only works for python 2.7 and later
    test_suite = test_loader.discover('.')
    return test_suite

def run():
    runner = unittest.TextTestRunner(descriptions=True, verbosity=2)
    suite = get_suite()
    # run the test suite
    return runner.run(suite)

if __name__ == '__main__':
    run()
