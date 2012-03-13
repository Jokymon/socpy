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

from socpy.processor import *
from socpy.foundation import SimulationObject

class ClassForTestingNamedInstructions(metaclass = SimulationObject):
    
    @instruction("instruction format", "instruction register", field1=1, field2=2)
    def an_instruction(self, parameter):
        return parameter

def test_instruction():
    @instruction("Instruction format", "Instruction register", field1=1, field2=2)
    def test_function(a, b):
        return a+b
    
    # the original functionality of the decorated function shouldn't change
    assert test_function(3, 5) == 8

    assert test_function.__instruction_format__ == "Instruction format"
    assert test_function.__instruction_register__ == "Instruction register"
    assert test_function.__matching__["field1"] == 1
    assert test_function.__matching__["field2"] == 2

def test_instruction_is_named():
    simulation_object = ClassForTestingNamedInstructions()
    assert simulation_object.an_instruction.name == "an_instruction"

def test_parameter_handling():
    """Making sure that member functions are properly wrapped with correct handling of self"""
    simulation_object = ClassForTestingNamedInstructions()
    assert simulation_object.an_instruction(42) == 42
