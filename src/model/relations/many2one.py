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


"""This module contains the class Many2OneRelation, described below."""

from model.relations.base import Relation

class Many2OneRelation(Relation):

    """Abstract class defining a many-to-one relation.

    This relation is used when the owning side defines a HasMany field type
    and the inverse side defines a HasOne field type.  If the relation
    is bidirectional (the default), then the inverse relation is a One2Many.

    """

    name = "many2one"
    def change_owner(self, model_object, indices_or_slice, new_values):
        """Change the owning's side.

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
            for model_object in self.owner.get_cache(model_object).mirror[ \
                    indices_or_slice]:
                self.set_value(model_object, self.inverse.field_name, None)

            del self.owner.get_cache(model_object).mirror[indices_or_slice]
        else:
            try:
                old_values = self.owner.get_cache(model_object).mirror[ \
                        indices_or_slice]
                assert old_values
            except (IndexError, AssertionError):
                # The new values are being added
                for value in new_values:
                    self.owner.get_cache(model_object).mirror.append(value)
                    self.set_value(value, self.inverse.field_name,
                            self.inverse)
            else:
                # Mere modification
                for value in old_values:
                    self.set_value(value, self.inverse.field_name, None)
                for value in new_values:
                    self.set_value(value, self.inverse.field_name,
                            self.inverse)
                self.owner.get_cache(model_object).mirror[ \
                        indices_or_slice] = values

    def change_inverse(self, model_object, new_inverse):
        """Change the inverse of the relation.

        The inverse is ALWAYS a single object, as this is a many2one relation.
        The 'one' part indicates that the inverse's side is always a single
        model object.

        Therefore, this method:
            Delete the previous inverse if needed
            Change the inverse's side
            Add the new inverse to the many side.

        """
        #if self.inverse:
        #    self.owner.get_cache(model_object).mirror.remove(model_object)

        self.set_value(model_object, self.inverse.field_name,
                new_inverse)
        self.owner.get_cache(model_object).mirror.append(new_inverse)

    def retrieve_objects(self, model_object):
        """Retrieve the objects of the many part.

        A Mayn2One relation uses the repository manager to retrieve
        a list of objects.

        """
        from model.functions import get_pkey_values
        value = get_pkey_values(model_object)
        if len(value) == 1:
            value = value[0]

        field = self.inverse.related_field
        repository = self.inverse.model._repository
        repository_manager = repository.data_connector.repository_manager
        return repository_manager.find_matching_objects(field, value)
