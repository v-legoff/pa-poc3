# Copyright (c) 2012 LE GOFF Vincent
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


"""This module defines the Model class, described below."""

from collections import OrderedDict

from model.functions import *
from model.meta import MetaModel
from model.types import *

class Model(metaclass=MetaModel):

    """Abstract class for a model.

    Each model must inherit from it.  This class is connected to a
    repository.  This repository will communicate with the data connector
    (the database, if configured) but the Model class SHOULD NOT use
    the repository directly, except from listeners.

    Remember that a Model object is a model's representation, not
    a line in your database or storage file.

    Each column is defined in the class body.  For instance:
    >>> class User(Model):
    ...     '''A model for an user.'''
    ...     username = String(max_size=30)
    ...     password = String(max_size=255)  # hashed password
    ...     creation_date = Datetime()
    ...

    """

    _repository = None
    bundle = None

    # Default fields
    id = Integer(pkey=True, auto_increment=True)

    def __init__(self, **kwargs):
        """Create an object from keyword arguments.

        Each keyword argument should be a field's name.  The
        'auto increment' fields SHOULD NOT be present.  Some may be
        omited, if they have default values.

        """
        self._cache = {}
        fields = get_fields(type(self))
        fields = dict((field.field_name, field) for field in fields)
        for name, value in kwargs.items():
            object.__setattr__(self, name, value)

        # Get the default values
        for name, field in fields.items():
            if not field.auto_increment and not name in kwargs and \
                    field.set_default:
                default = field.default
                if default is None:
                    raise ValueError("the field {} of model {} has no " \
                            "default value".format(field.field_name,
                            type(self)))
                elif callable(default):
                    default = default(self)

                object.__setattr__(self, name, default)

    def __repr__(self):
        pkeys = get_pkey_values(self)
        pkeys = [repr(field) for field in pkeys]
        pkeys = " ".join(pkeys)
        return "<model {} ({})>".format(get_name(type(self)), pkeys)

    def __setattr__(self, attr, value):
        """Set the value to the field.

        This method checks the value type as well.

        """
        try:
            field = getattr(type(self), attr)
        except AttributeError:
            object.__setattr__(self, attr, value)
            return

        if isinstance(field, BaseType) and field.register:
            # Check the value type
            check = field.accept_value(value)

        old_value = getattr(self, attr)
        object.__setattr__(self, attr, value)
        if isinstance(old_value, BaseType):
            # Not set yet
            old_value = None

        if field.register and self._repository and \
                is_built(self):
            self._repository.update(self, attr, old_value)

    # Methods to represent objects
    def display_representation(self, filters=None):
        """Return a dict containing the filtered self.__dict__."""
        attrs = OrderedDict()
        for field in get_fields(type(self)):
            name = field.field_name
            value = getattr(self, name)
            attrs[name] = value

        if filters is None:
            return attrs
        elif isinstance(filters, list):
            filter_attrs = OrderedDict()
            for attr in filters:
                if attr in attrs:
                    filter_attrs[attr] = attrs[attr]
            return filter_attrs
