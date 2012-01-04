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

from socpy.types import InstFormat, Unsigned

def test_InstFormat():
    test_format = InstFormat(
        ('field1', Unsigned(2)),
        ('field2', Unsigned(3)),
        ('field3', Unsigned(4))
    )

    assert test_format.size == 9

    assert test_format.fields[0].mask == 0x180
    assert test_format.fields[0].position == 7
    assert test_format.fields[0].name == "field1"

    assert test_format.fields[1].mask == 0x70
    assert test_format.fields[1].position == 4
    assert test_format.fields[1].name == "field2"

    assert test_format.fields[2].mask == 0xf
    assert test_format.fields[2].position == 0
    assert test_format.fields[2].name == "field3"

def test_InstFormat_get_mask():
    test_format = InstFormat(
        ('field1', Unsigned(2)),
        ('field2', Unsigned(3)),
        ('field3', Unsigned(4))
    )

    mask1 = test_format.get_mask(field3=0)
    assert mask1 == 0xf

    mask2 = test_format.get_mask(field1=2)
    assert mask2 == 0x180

def test_InstFormat_get_value():
    test_format = InstFormat(
        ('field1', Unsigned(2)),
        ('field2', Unsigned(3)),
        ('field3', Unsigned(4))
    )

    value1 = test_format.get_value(field3=4)
    assert value1 == 4

    value2 = test_format.get_value(field2=7)
    assert value2 == 0x70

