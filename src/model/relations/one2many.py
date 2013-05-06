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


"""This module contains the class One2ManyRelation, described below."""

from model.relations.base import Relation

class One2ManyRelation(Relation):

    """Abstract class defining a one-to-many relation.

    This relation is used when the owning side defines a HasOne field type
    and the inverse side defines a HasMany field type.  If the relation
    is bidirectional (the default), then the inverse relation is a Many2One.

    """

    name = "one2many"
    def change_owner(self, model_object, new_owner):
        """Change the owner of the relation.

        The owner is ALWAYS a single object, as this is a one2many relation.
        The 'one' part indicates that the owner's side is always a single
        model object.

        Therefore, this method:
            Delete the previous owner if needed
            Change the owner's side
            Add the new owner to the many side.

        """
        if model_object in self.inverse.get_cache(model_object).mirror:
            self.inverse.get_cache(model_object).mirror.remove(self.owner)

        self.inverse.get_cache(model_object).mirror.append(new_owner)

    def change_inverse(self, model_object, indices_or_slice, new_values):
        """Change the inverse's side.

        We need:
            The indices or slice that changed
            The new value(s).

        If the values only contain None object, then it's a deletion.  If
        it's an addition, then the indices are just outside of the field's
        indices.  If it's a mere modification, the indices are present
        in the field.

        """
        indicesor_slice, new_values = self.convert_to_list(indice_or_slices,
                new_values)
        if all(value is None for value in new_values):
            # Deletion
            for model_object in self.inverse.get_cache(model_object).mirror[ \
                    indices_or_slice]:
                self.set_value(model_object, self.owner.field_name, None)

            del self.inverse.get_cache(model_object).mirror[indices_or_slice]
        else:
            try:
                old_values = self.inverse.get_cache(model_object).mirror[ \
                        indices_or_slice]
                assert old_values
            except (IndexError, AssertionError):
                # The new values are being added
                for value in new_values:
                    self.inverse.get_cache(model_object).mirror.append(value)
                    self.set_value(value, self.owner.field_name, self.inverse)
            else:
                # Mere modification
                for value in old_values:
                    self.set_value(value, self.owner.field_name, None)
                for value in new_values:
                    self.set_value(value, self.owner.field_name, self.inverse)
                self.inverse.get_cache(model_object).mirror[ \
                        indices_or_slice] = new_values

    def extend(self):
        """Extend if necessary one of the model."""
        from model.functions import get_pkey_names
        attribute_name = self.owner.attribute_name
        pkey_names = get_pkey_names(self.inverse.model)
        if len(pkey_names) > 1:
            raise ValueError("more than one foreign key for this relation " \
                    "is not valid")

        pkey = pkey_names[0]
        field_type = type(getattr(self.inverse.model, pkey))
        if not field_type.can_relate:
            raise ValueError("the type of field {} can't be used in " \
                    "a relation".format(field_type))

        related = field_type(default=lambda o: None)
        related.field_name = attribute_name
        related.model = self.owner.model
        related.set_default = False
        setattr(self.owner.model, attribute_name, related)
