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


"""This module contains the DCMirror class, detailed below."""

import collections

class DCMirror(collections.MutableSequence):

    """Class used to represent a mirror on a list.

    A mirrored list is basically a list of model objects.  You can manipulate it
    as a a standard list though (adding new model objects, remove them or
    updating them).  The only thing it will do will be to transform the
    model objects into something it could store (like an ID).

    """

    def __init__(self, field):
        self.elements = []
        self.field = field

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, i):
        values = self.get_models()
        return values[i]

    def __delitem__(self, i):
        del self.elements[i]

    def __setitem__(self, i, values):
        values = self.check(values)
        self.elements[i] = values

    def insert(self, i, value):
        value = self.check(value)
        self.elements.insert(i, value)

    def __repr__(self):
        values = self.get_models()
        return repr(values)

    def __str__(self):
        values = self.get_models()
        return str(values)

    @property
    def repository(self):
        """Return the model's repository."""
        return self.field.model._repository

    def get_models(self):
        """Return the corresponding models."""
        models = []
        repository = self.repository
        for element in self.elements:
            model_object = repository.find(element)
            models.append(model_object)

        return models

    def check(self, values):
        """Check that the value(s) are of the right type."""
        from model.functions import get_pkey_values
        model = self.field.model
        if isinstance(values, list):
            if not all(isinstance(value, model) for value in values):
                raise ValueError("this mirror list doesn't accept this " \
                        "type of datas")

            results = []
            for value in values:
                pkey_values = get_pkey_values(value)
                if len(pkey_values) == 1:
                    pkey_values = pkey_values[0]

                results.append(pkey_values)

            return results

        if not isinstance(values, model):
            raise ValueError("this mirror list doesn't accept this type " \
                    "of data")

        pkey_values = get_pkey_values(values)
        if len(pkey_values) == 1:
            pkey_values = pkey_values[0]

        return pkey_values
