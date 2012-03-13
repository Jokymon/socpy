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
    def __init__(self, function_ast, inst_format, inst_reg, matching, wrappee):
        self.__function_ast__ = function_ast
        self.__instruction_format__ = inst_format
        self.__instruction_register__ = inst_reg
        self.__matching__ = matching
        self.behavior = wrappee
        self.owner = None

    def __call__(self, *args, **kwargs):
        if self.owner:
            return self.behavior(self.owner, *args, **kwargs)
        else:
            return self.behavior(*args, **kwargs)

class InstructionMember(SimulationObjectMember):
    def __init__(self, function_ast, inst_format, inst_reg, matching, wrappee):
        self.instance = InstructionBehavior(function_ast, inst_format, inst_reg, matching, wrappee)

    def __get__(self, obj, objtype):
        self.instance.owner = obj
        return self.instance

    def __call__(self, *args, **kwargs):
        return self.instance(*args, **kwargs)

    def __setattr__(self, key, value):
        if key!="instance":
            SimulationObjectMember.__setattr__(self.instance, key, value)
        SimulationObjectMember.__setattr__(self, key, value)

    def __getattr__(self, key):
        return getattr(self.instance, key)
        
def instruction(instruction_format, instruction_register, **kwargs):
    def create_wrapped(func):
        source = inspect.getsource(func)
        source = textwrap.dedent( source )
        wrapped = InstructionMember(
            ast.parse( source ),
            instruction_format,
            instruction_register,
            kwargs,
            func)
        wrapped.behavior = func
        return wrapped
    return create_wrapped

