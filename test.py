########################################################################
#
# This file is part of SocPy.
# 
# SocPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# SocPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with SocPy.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

import os, os.path, sys
import unittest

# import all modules in the test directory
modules = os.listdir("test")
for m in filter(lambda x: x.endswith(".py"), modules):
    if m.startswith("__"):
        continue
    __import__("test." + m[:m.rfind(".")])

# find all test_... functions in the imported modules

test_cases = []

test = sys.modules["test"]
for name in filter(lambda x: not x.startswith("__"), 
                         dir(test)):
    sub_module = test.__dict__[name]
    for sym in filter(lambda x: x.startswith("test_"),
                            dir(sub_module)):
        func = sub_module.__dict__[sym]
        test_cases.append(func)

# create test cases out of the functions collected before
all_tests = unittest.TestSuite( 
                map(unittest.FunctionTestCase, test_cases)
            )
unittest.TextTestRunner().run(all_tests)

