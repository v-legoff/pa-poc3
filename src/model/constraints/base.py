# Copyright (c) 2013 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""This module contains the BaseConstraint abstract class, defined below."""

class BaseConstraint:

    """Class representing a model type constraint.

    There should exist a constraint per model type.  For instance, the
    Integer model type should have a constraint with different
    parameters.  The String model type could have a constraint with
    'min_length', 'max_length' and so on.

    """

    name_type = "undefined"
    constraints = []
    def __init__(self, base_type):
        self.base_type = base_type

    def __str__(self):
        return type(self).name_type + " " + self.constraints_on(
                *type(self).constraints)

    def has(self, name):
        """Return True if this constraint is ON."""
        return hasattr(self, name) and getattr(self, name)

    def constraint_on(self, name):
        """Return whether the constraint is on or off.

        Return values:
            name -- the constraint is ON
            False -- the constraint is OFF
            some value -- the constraint as a specific argument.

        """
        value = getattr(self, name)
        if isinstance(value, bool):
            if value:
                return name
            else:
                return False
        else:
            return name + " " + repr(value)

    def constraints_on(self, *names):
        """Display a list of constraints."""
        constraints = []
        for name in names:
            value = self.constraint_on(name)
            if value:
                constraints.append(value)

        return ", ".join(constraints)

    def control(self, value):
        """Return whether the value is correct for these constraints."""
        return True
