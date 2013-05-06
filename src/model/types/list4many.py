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


"""This module contains the List4Many class, described below."""

from model.representations.dc_mirror import DCMirror

class List4Many(DCMirror):

    """Class used to represent a mirror on a list, like DCMirror itself.

    This class does something more, though, as it is used to trigger
    the other side of a relation.  This type is used as a representation
    for a *many relation (the HasMany field type).

    """

    def __init__(self, mirror, model_object):
        self.mirror = mirror
        self.elements = mirror.elements
        self.field = mirror.field
        self.model_object = model_object

    def __delitem__(self, i):
        relation = self.field.relation
        if isinstance(i, int):
            relation.change_owner(self.model_object, i, None)
        elif isinstance(i, slice):
            if i.start is not None and i.stop is not None:
                values = [None] * (i.stop - i.start)
            elif i.start is not None:
                values = [None] * (len(self.elements) - i.start)
            else:
                values = [None] * len(self.elements)

            relation.change_owner(self.model_object, i, values)

        DCMirror.__delitem__(self, i)

    def __setitem__(self, i, values):
        relation = self.field.relation
        relation.change_owner(self.model_object, i, values)
        DCMirror.__setitem__(self, i, values)

    def insert(self, i, value):
        relation = self.field.relation
        relation.change_owner(self.model_object, i, value)
        DCMirror.__setitem__(self, i, values)
