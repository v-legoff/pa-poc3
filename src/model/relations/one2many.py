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
    def affect(self, model_object, old_value, new_value):
        """Change the value on the inverse's side.

        The owning's side has been changed.  This method is used to
        apply this change to the inverse's side.  This is a One2Many
        relation, therefore the owning's side is a single object.
        The inverse's side is a list (the many's part) so we delete
        the old owner, if it exists, and add the new one.

        """
        old_mirror = old_value is not None and self.inverse.get_cache(
                old_value).mirror or None
        new_mirror = self.inverse.get_cache(new_value).mirror if \
                new_value else None
        if old_mirror and model_object in old_mirror:
            old_mirror.remove(model_object)

        if new_mirror is not None:
            new_mirror.append(model_object)

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
