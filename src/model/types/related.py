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


"""This module contains the Related abstract class, defined below."""

from model.relations.one2many import One2ManyRelation
from model.relations.many2one import Many2OneRelation
from model.types.base import BaseType

class Related(BaseType):

    """Class representing an abstract relation to another model.

    The 'has_one', 'has_many' and 'belong_to' field types should inherit
    from this class.  It contains several methods that are useful for
    creation relations.

    """

    nb_doreign_models = None
    def __init__(self):
        BaseType.__init__(self, pkey=False, default=None)
        self.register = False
        self.foreign_model = None

    def find_relation(self):
        """Find and return the relation.

        First we select the type of this field.  Next we try to find an
        inverse relation field in the foreign model.  With them, we can
        create one or two relations (bidirectional relations are two
        relations bound together).  For instance, if the 'self' field
        type is a 'has_one' and the foreign model has a 'has_many'
        pointing to the original model, then we create a
        'One2ManyRelation' between 'self' and the foreign model and an
        inverse relation ('Many2OneRelation') between the foreign model
        and 'self'.

        """
        from model.functions import get_fields, get_name
        nb_self = self.nb_foreign_models
        if isinstance(self.foreign_model, str):
            self.foreign_model = self.model._repository.get_model(
                    self.foreign_model)

        # Now we try to find the inverse field
        foreign_fields = get_fields(self.foreign_model, register=False)
        foreign_fields = [field for field in foreign_fields if \
                field is not self]
        foreign_field = None
        for field in foreign_fields:
            if isinstance(field, Related) and (get_name(
                    self.model) == field.foreign_model or isinstance(
                    field.foreign_model, type(self.model))):
                foreign_field = field
                foreign_field.foreign_model = self.model
                break

        if foreign_field is None:
            raise ValueError("the foreign field for the {}.{} field " \
                    "cannot be found in {}".format(self.model,
                    self.field_name, self.foreign_model))

        nb_foreign = foreign_field.nb_foreign_models

        cls_relation = None
        cls_inverse_relation = None
        if nb_self == 0:
            return None
        elif nb_self == -1:
            if nb_foreign == 1:
                cls_relation = Many2OneRelation
                cls_inverse_relation = One2ManyRelation
            elif nb_foreign == -1:
                # many2many
                pass
            else:
                cls_relation = Many2OneRelation
        else:
            if nb_foreign == 1:
                # one2one
                pass
            elif nb_foreign == -1:
                cls_relation = One2ManyRelation
                cls_inverse_relation = Many2OneRelation
            else:
                # one2one
                pass

        relation = cls_relation(self, foreign_field)
        if cls_inverse_relation:
            inverse_relation = cls_inverse_relation(foreign_field, self)
            inverse_relation.inverse_relation = relation
            relation.inverse_relation = inverse_relation

        return relation
