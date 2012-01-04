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
from socpy.types import Unsigned, InstFormat
from socpy.processor import instruction, mnemonic
from socpy.hardware import Processor, Memory, RegisterBank, Register, InstructionPointer

class Mips(Processor):
    main_memory = Memory( 65536, Unsigned(32) )
    ir = InstructionPointer( Unsigned(32), main_memory )

    r = RegisterBank( 32, Unsigned(32) )
    hi = Register( Unsigned(32) )
    lo = Register( Unsigned(32) )

    I_Type = InstFormat(
        ('op',        Unsigned(6)),
        ('rs',        Unsigned(5)),
        ('rt',        Unsigned(5)),
        ('immediate', Unsigned(16))
    )

    R_Type = InstFormat(
        ('op',          Unsigned(6)),
        ('rs',          Unsigned(5)),
        ('rt',          Unsigned(5)),
        ('rd',          Unsigned(5)),
        ('sa',          Unsigned(5)),
        ('funct',       Unsigned(6))
    )

    @instruction( R_Type, ir, op=0, rs=0, rt=0, rd=0, sa=0, funct=0x0)
    @mnemonic( "nop" )
    def nop():
        pass

    @instruction( R_Type, ir, op=0, sa=0, funct=0)
    @mnemonic( "move" )
    def move():
        pass

    @instruction( R_Type, ir, op=0, sa=0, funct=0x20)
    @mnemonic( "add {rd}, {rs}, {rt}" )
    #or: "add", "rd":Register, "rs":Register   ??
    def add():
        pass

    @instruction( R_Type, ir, op=0, sa=0, funct=0x24)
    @mnemonic( "and {rd}, {rs}, {rt}" )
    def and_instr():
        pass

    @instruction( I_Type, ir, op=9 )
    @mnemonic( "addiu {rt}, {rs}, {imm}" )
    def addiu(self, **kwargs):
        pass

if __name__=="__main__":
    m = Mips()
    
    #print(m.r)
    #m.run()
    print( m.I_Type )
    m.hi = 4
    print( m.main_memory )
    m.generate_simulator("mips_test.cpp")
