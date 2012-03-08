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

from socpy.foundation import SimulationObjectMember
import textwrap
import inspect, ast

class InstructionBehavior(SimulationObjectMember):
    def __init__(self, function_ast, inst_format, inst_reg, matching):
        self.__function_ast__ = function_ast
        self.__instruction_format__ = inst_format
        self.__instruction_register__ = inst_reg
        self.__matching__ = matching

    def __call__(self, *args, **kwargs):
        return self.behavior(*args, **kwargs)
        
def instruction(instruction_format, instruction_register, **kwargs):
    def create_wrapped(func):
        source = inspect.getsource(func)
        source = textwrap.dedent( source )
        wrapped = InstructionBehavior(
            ast.parse( source ),
            instruction_format,
            instruction_register,
            kwargs)
        wrapped.behavior = func
        return wrapped
    return create_wrapped

