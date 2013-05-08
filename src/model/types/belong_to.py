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


"""This module contains the BelongTo relation field type."""

from model.types.has_one import HasOne
from model.types.related import Related

class BelongTo(Related):

    """Class representing a belong_to relation.

    The 'belong_to' field is very similar to the 'has_one' field,
    but it is used to create a unidirectional many2one relation.
    If you define a field 'belong_to' like this:
        class Comment(Model):
            post = BelongTo("bundle.Post")

        class Post(Model):
            comments = HasMany("bundle.Comment")

    Then you won't be able to query the specified post of a comment:
    >>> comment.post
        ...
    TypeError: you cannot query from this field

    But you will be able to query the comments of a post:
    >>> post.comments
    [...]

    In short, this field is useful if you want to create a many2one
    relation without one2many inverse relation (a unidirectional
    relation).

    """

    type_name = "belong_to"
    nb_foreign_models = 0
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

    get_related = HasOne.get_related
    set_related = HasOne.set_related
    extend = HasOne.extend

    def __get__(self, obj, typeobj):
        """Forbidden, raise an exception."""
        if obj is None:
            return self

        raise TypeError("you cannot query from this field")

    def __set__(self, obj, new_obj):
        """Forbidden : raise an exception."""
        raise TypeError("you cannot set this field")
