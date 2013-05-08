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
    def affect(self, model_object, indice_or_slice, old_values, new_values,
            mod_type):
        """Affect the inverse's side (a single object).

        Depending on the mod_type attribute (delete, add or modify),
        different actions are performed.  In any case, the List4Many
        representing the many's part of this relation (the owning's side)
        affects the inverse's side (the one part of the many2one
        relation).  If the model is deleted, then the related is set
        to None.  If not, the old_values are updated to match the
        corresponding actions.

        """
        indice_or_slice, old_values = self.convert_to_list(indice_or_slice,
                old_values)
        if new_values is not None and not isinstance(new_values, list):
            new_values = [new_values]

        if mod_type == Relation.TYPE_DELETE:
            for old_object in old_values:
                self.inverse.set_related(old_object, None)
            return

        if mod_type == Relation.TYPE_MODIFY:
            for old_object in old_values:
                if old_object not in new_values:
                    self.inverse.set_related(old_object, None)

        if mod_type in [Relation.TYPE_MODIFY, Relation.TYPE_ADD]:
            for new_object in new_values:
                self.inverse.set_related(new_object, model_object)

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

    def extend(self):
        """Extend if necessary one of the model."""
        from model.functions import get_pkey_names
        attribute_name = self.inverse.attribute_name
        pkey_names = get_pkey_names(self.owner.model)
        if len(pkey_names) > 1:
            raise ValueError("more than one foreign key for this relation " \
                    "is not valid")

        pkey = pkey_names[0]
        field_type = type(getattr(self.owner.model, pkey))
        if not field_type.can_relate:
            raise ValueError("the type of field {} can't be used in " \
                    "a relation".format(field_type))

        related = field_type(default=lambda o: None)
        related.field_name = attribute_name
        related.model = self.inverse.model
        if self.inverse_relation: #  didirectional
            related.set_default = False
        setattr(self.inverse.model, attribute_name, related)
