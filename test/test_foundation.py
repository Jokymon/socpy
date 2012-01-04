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

from socpy.foundation import SimulationObject, SimulationObjectMember

class MockMember(SimulationObjectMember):
    pass

class MetaClassMember(metaclass = SimulationObject):
    def __init__(self):
        self.meta_class_init_called = True

class MetaSubClass(MetaClassMember):
    def __init__(self):
        super(MetaSubClass, self).__init__()
        self.meta_subclass_init_called = True

class ClassForTestingMetaClass(metaclass = SimulationObject):
    member1 = MockMember()
    member2 = MetaClassMember()

#########################################################

def test_SimulationObject_members_get_name():
    a_instance = ClassForTestingMetaClass()
    assert a_instance.member1.name == "member1"
    assert a_instance.member2.name == "member2"

def test_SimulationObject_init_called():
    # SimulationObject replaces the __init__ function, however the original
    # __init__ function should still be called
    sub_object = MetaSubClass()

    assert sub_object.meta_class_init_called
    assert sub_object.meta_subclass_init_called
