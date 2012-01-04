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

class ProcessorDefinition(SimulationObjectMember):
    def __init__(self):
        self.name = ""

class DataType(ProcessorDefinition):
    def __init__(self):
        super(DataType, self).__init__()

class Unsigned(DataType):
    def __init__(self, size=32):
        self.size=size

    def __repr__(self):
        return "Unsigned(%u)" % self.size

class FormatField(ProcessorDefinition):
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype
        self.mask = 0x0
        self.position = -1

    def size(self):
        return self.datatype.size

    def c_type(self):
        if isinstance(self.datatype, Unsigned):
            return "uint32_t"
        else:
            return "int32_t"

    def __repr__(self):
        return "%s: %s, %u, %x" % (self.name, self.datatype, self.position, self.mask)

class InstFormat(ProcessorDefinition):
    def __init__(self, *args, **kwargs):
        super(InstFormat, self).__init__()
        position = 0
        fields = []
        for field in args[::-1]:
            mask = ((2 ** field[1].size)-1) << position
            field = FormatField( *field )
            field.mask = mask
            field.position = position
            fields.insert( 0, field )
            position += field.size()

        self.size = position
        self.fields = fields

    def get_mask(self, **matching):
        mask = 0
        for (key, val) in matching.items():
            for field in self.fields:
                if key==field.name:
                    mask |= field.mask
        return mask

    def get_value(self, **matching):
        value = 0
        for (key, val) in matching.items():
            for field in self.fields:
                if key==field.name:
                    value |= val << field.position
        return value

    def __repr__(self):
        s = "Format '%s' of size %u\n" % (self.name, self.size)
        for field in self.fields:
            s += "%s\n" % field
        return s

