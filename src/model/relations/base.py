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


"""This module contains the abstract class Relation, described gbelow."""

class Relation:

    """Abstract tlcass defining a standard relation.

    Whatever the relation, it implies two models:  the first one is
    on the owning side of the relation, the second one is on the inverse
    side.  This notion is abstracted by the relation abstract class
    (and its subclasses) and SHOULD NOT be used directly by the user.
    Instead, she will use the field types:
        HasOne -- the model is related to ANOTHER ONE
        HasMany -- the model is connected with MANY other model objects
        BelongTo -- like has one but without relation usable on this side

    These two fields are used to create in the background a relation.
    For instance:
        class Post(Model):
            title = String()
            published_at = DateTime()
            comments = HasMany("bundle.Comments")

        class Comment(Model):
            author = String()
            content = String()
            post = HasOne("bundle.Post")

    This code will create a One2Many relation between the comment and post
    (comment HAS ONE post) and a Many2One relation between the post and
    comment (post HAS MANY comments).

    By default, that means that a relation is bidirectional.  The BelongTo
    field type allows to create unidirectional relations.  If, for instance,
    you replace the:
            post = HasOne("bundle.Post")
    line by:
            post = BelongTo("bundle.Post")
    then you won't be able to do something like:
        post = comment.post  # unidirectional, impossible like this

    """

    name = "unknown relation"

    # Constants
    TYPE_DELETE = 0
    TYPE_MODIFY = 1
    TYPE_ADD = 2

    def __init__(self, owner, inverse):
        self.owner = owner
        self.inverse = inverse
        self.inverse_relation = None  # set if the relation is bidirectional

    def __repr__(self):
        from model.functions import get_name
        rel_type = type(self).name
        owner = get_name(self.owner.model)
        field = self.owner.field_name
        inverse_field = self.inverse.field_name
        inverse = get_name(self.inverse.model)
        if self.inverse_relation:
            return "<bidirectional {} between {}.{} and {}.{}>".format(
                    rel_type, owner, field, inverse, inverse_field)
        else:
            return "<unidirectional {} between {}.{} and {}.{}>".format(
                    rel_type, owner, field, inverse, inverse_field)

    def convert_to_list(self, indices_or_slice, values):
        """Convert the value into a list of values.

        If the indices_or_slice parameter is an integer, return a slice
        containing this integer.

        """
        if isinstance(indices_or_slice, int):
            if indices_or_slice == -1:
                return slice(indices_or_slice, None), [values]

            return slice(indices_or_slice, indices_or_slice + 1), [values]

        return indices_or_slice, values

    def extend(self):
        """Extend one of the model if necessary."""
        pass

    def affect(self):
        """This method is used to apply the changes to the inverse.

        This method could take different parameters depending on
        the relation type.  Either:
            model_object -- the changed model object
            old_value -- the old value assigned to the owner's field
            new_value -- te new value assigned to the owner's field
        Or:
            model_object -- the modified owner
            indices_or_slice -- the indices or slice of the modification
            old_values -- the old values (if modified or deleted)
            new_values -- the new values (could be None if mod_type is DELETE)
            mod_type -- the type of moficiation (DELETE, MODIFICATION, ADD)

        This method should be called AFTER the owner's modification.

        """
        pass
