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


"""This module contains the HasMany relation field type."""

from model.representations.dc_mirror import DCMirror
from model.types.list4many import List4Many
from model.types.related import Related

class HasMany(Related):

    """Class representing a has_many relation.

    Here is a snippet of code using relations:
        class User(Model):
            username = String()
            groups = HasMany("user.Group")

    When a relation HasMany is created, it creates in the foreign model's table
    a transparent new attribute containing a referrence to the current
    model.  The mechanism is described in the model.relations.one2many
    module.

    """

    type_name = "has_many"
    nb_foreign_models = -1 # Infinite
    def __init__(self, foreign_model):
        Related.__init__(self)
        self.set_default = False
        self.foreign_model = foreign_model
        self.relation = None

    def extend(self):
        """Extend the model."""
        # First we create the relation if necessary
        if self.relation is None:
            relation = self.find_relation()
            self.relation = relation
            if self.relation.inverse_relation:
                relation.inverse.relation = relation.inverse_relation

            print("Create relation", self.relation)
        self.relation.extend()

    def __get__(self, obj, typeobj):
        """Try to access the related value."""
        if obj is None:
            return self

        elements = self.get_cache(obj)
        return elements

    def __set__(self, obj, new_obj):
        """Try to set the related value.

        Simply update the lists.

        """
        elements = self.get_cache(obj)
        elements[:] = new_obj

    def get_cache(self, obj):
        """Return the cached list or create the List4Many if needed."""
        field = self.field_name
        if field in obj._cache:
            return obj._cache[field]

        mirror = DCMirror(self)
        elements = List4Many(mirror, obj)
        obj._cache[field] = elements
        return elements
