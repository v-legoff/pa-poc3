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


"""This module contains the HasOne relation field type."""

from model.types.base import BaseType
from model.types.related import Related

class HasOne(Related):

    """Class representing a has_one relation.

    Here is a snippet of code using relations:
        class User(Model):
            username = String()
            group = HasOne("user.Group")

    When a relation HasOne is created, it creates in the model's table
    a transparent new attribute containing a single referrence to an
    object (or None).  This relation is not visible (and should not be
    used directly) by the user.  The original attribute is a descriptor
    which will fetch the required object, using the repository.  Here's
    a snipset using the User model defined above:
    >>> me = User.find(id=1)  # it exists
    >>> print(me.group_id)
    None
    >>> me.group_id = 1 # change the group
    >>> me.group_id
    1
    >>> me.group
    <user.Group model object>
    >>> me.group.name
    "the first group"
    >>> me.group = Group.find(id=2)
    >>> me.group.name
    "the second group"
    >>> me.group_id
    2

    """

    type_name = "has_one"
    nb_foreign_models = 1
    def __init__(self, foreign_model, attribute_name=None):
        Related.__init__(self)
        self.foreign_model = foreign_model
        self._attribute_name = attribute_name
        self.relation = None
        self.set_default = False

    @property
    def attribute_name(self):
        """Return the attribute name if set, otherwise a default one."""
        if self._attribute_name:
            return self._attribute_name

        attribute_name = self.field_name + "_id"
        return attribute_name

    @property
    def related_field(self):
        """Return the related field."""
        return getattr(self.model, self.attribute_name)

    def get_related(self, obj):
        """Return the link to the related_to field."""
        attribute_name = self.attribute_name
        return getattr(obj, attribute_name)

    def set_related(self, obj, new_obj):
        """Set the related field.

        The value should be a model object.

        """
        from model.functions import get_pkey_values
        attribute_name = self.attribute_name
        model = self.foreign_model
        if new_obj is None:
            new_value = None
        else:
            if not isinstance(new_obj, model):
                raise ValueError("try to affect {} to the {}.{} model " \
                        "field".format(new_obj, self.model, self.field_name))

            values = get_pkey_values(new_obj)
            if len(values) == 1:
                values = values[0]

            new_value = values

        setattr(obj, attribute_name, new_value)

    def extend(self):
        """Extend the model."""
        # First we create the relation if necessary
        if self.relation is None:
            relation = self.find_relation()
            self.relation = relation
            if self.relation and self.relation.inverse_relation:
                relation.inverse.relation = relation.inverse_relation
        if self.relation:
            self.relation.extend()

    def __get__(self, obj, typeobj):
        """Try to access the related value."""
        if obj is None:
            return self

        key = self.get_related(obj)
        repository = self.foreign_model._repository
        if key is None or isinstance(key, BaseType):
            return None

        return repository.find(key)

    def __set__(self, obj, new_obj):
        """Try to set the related value.

        We change the attribute_name value on the object depending on the
        given new_obj's primary keys.

        """
        old_value = getattr(obj, self.field_name)
        self.set_related(obj, new_obj)
        self.relation.affect(obj, old_value, new_obj)
