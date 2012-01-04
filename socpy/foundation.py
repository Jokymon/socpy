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

class SimulationObjectMember(object):
    pass

class SimulationObject(type):
    def __new__(cls, name, bases, dct):
        return type.__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super(SimulationObject, cls).__init__(name, bases, dct)
        for (key, value) in dct.items():
            metaclassname = value.__class__.__class__.__name__
            if metaclassname == "SimulationObject" or isinstance(value, SimulationObjectMember):
                value.name = key

        def __init__(self, *args, **kwargs):
            if hasattr(self, "_old_init__"):
                cls._old_init__(self, *args, **kwargs)
        if hasattr(cls, "__init__"):
            cls._old_init__ = cls.__init__
        cls.__init__ = __init__


