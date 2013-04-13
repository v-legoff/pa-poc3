# Copyright (c) 2012 LE GOFF Vincent
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


"""This module contains the abstract class BaseType."""

import copy

from model.constraints import CONSTRAINTS

class BaseType:

    """Class representing an abstract type of field.

    Each created field has a 'nid' attribute, which represent its identifier
    different from all other types, no matter the field type or the model
    in which it is defined.  This identifier is used to order the fields
    for an object.

    """

    current_nid = 1

    @classmethod
    def next_nid(cls):
        nid = BaseType.current_nid
        BaseType.current_nid += 1
        return nid

    type_name = "undefined"
    def __init__(self, default=None, **kwargs):
        """The basetype field constructor."""
        self.nid = self.next_nid()
        self.model = None
        self.field_name = "unknown name"
        self.default = default
        self.register = True
        self.set_default = True
        constraint = CONSTRAINTS.get(type(self).type_name)
        if constraint:
            constraint = constraint(self, **kwargs)

        self.constraint = constraint

    def __repr__(self):
        return "<field {} ({})>".format(repr(self.field_name), self.nid)

    def copy(self):
        """Return a shallow copy of self."""
        copied = copy.copy(self)
        copied.nid = self.next_nid()
        return copied

    def extend(self):
        """Extend the model if needed.

        This method is called after the copy of the new field.  That means
        that it is connected to a model (self.model points to a class,
        not to None) and you can use this instance attribute to extend
        the class.

        """
        pass

    def has_constraint(self, name):
        """Return whether the constraint is ON for this field."""
        return self.constraint and self.constraint.has(name)
