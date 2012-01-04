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

from socpy.types import Unsigned, InstFormat
from socpy.foundation import SimulationObject, SimulationObjectMember

class HardwareComponent(object, metaclass=SimulationObject):
    def __init__(self):
        self.name = ""

class Processor(HardwareComponent):
    def run(self):
        print("Running the processor")

    def get_formats(self):
        formats = {}
        for member_name in dir(self):
            if isinstance( getattr(self, member_name), InstFormat ):
                formats[member_name] = getattr(self, member_name)
        return formats

    def get_instructions_by_mask(self):
        instructions = {}
        for member_name in dir(self):
            member = getattr(self, member_name)
            if hasattr(member, "__matching__"):
                mask = member.__instruction_format__.get_mask( **member. __matching__ )
                key = (member.__instruction_register__, mask)
                if not key in instructions.keys():
                    instructions[key] = []
                instructions[key].append( member )
        return instructions

    def get_instruction_pointers(self):
        instruction_pointers = {}
        for member_name in dir(self):
            if isinstance( getattr(self, member_name), InstructionPointer ):
                instruction_pointers[member_name] = getattr(self, member_name)
        return instruction_pointers

    def generate_simulator(self, src_file):
        f = open(src_file, "w")
        f.write("void %s::executeInstruction()\n" % self.__class__.__name__)
        f.write("{\n")
        for (name, ir) in self.get_instruction_pointers().items():
            f.write("    uint32_t instruction_word_%s;\n" % name)
            f.write("    instruction_word_%s = %s.getData(%s);\n\n" % (name, ir.memory.name, name))
        for (name, format) in self.get_formats().items():
            f.write("    // Extractions for format %s\n" % name)
            for field in format.fields:
                # TODO: very evil: the variable name for the mask shouldn't be hardcoded here
                f.write("    %s %s_%s = (instruction_word_ir >> %u) & 0x%x;\n" % (
                    field.c_type(),
                    name,
                    field.name,
                    field.position,
                    field.mask>>field.position)
                )
        f.write("\n")
        for ( (ir, mask), instructions) in self.get_instructions_by_mask().items():
            f.write("    switch( %s & 0x%x) {\n" % (ir.name, mask) )
            for instruction in instructions:
                value = instruction.__instruction_format__.get_value( **instruction.__matching__ )
                f.write("        case 0x%x:\n" % (value, ) )
                f.write("            // implementation of %s\n" % instruction.name)
                f.write("            break;\n")
            f.write("    }\n")
        f.write("}\n")
        f.close()

class Memory(HardwareComponent):
    def __init__(self, count, data_type):
        self.data_type = data_type
        self.count = count

        from math import ceil, log
        address_size = int( ceil( log(count)/log(2) ) )
        self.address_type = Unsigned( address_size )

    def __repr__(self):
        return "Memory %s[%u] : %s" % (self.name, self.count, self.data_type)

class RegisterBank(HardwareComponent):
    def __init__(self, count, register_type):
        self.reg_type = register_type
        self.count = count

class Register(HardwareComponent):
    def __init__(self, register_type):
        self.reg_type = register_type

class InstructionPointer(Register):
    def __init__(self, register_type, memory):
        super(InstructionPointer, self).__init__(register_type)
        self.memory = memory


