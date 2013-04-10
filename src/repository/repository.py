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


"""Module containing the Repository class, described below."""

from collections import OrderedDict

from model import Model
from model.functions import *

class Repository:

    """The default repository class.

    A repository is bound to a model.  It is responsible for
    the communication with the data connector using generic
    methods.  It can also create and manage queries.  A model
    (model.Model class) MUST ALWAYS have a bound repository.
    If none is found, a default repository is created for this
    model.

    This class is the default repository structure.  If an
    user creates a model without creating a repository bound
    to it, this class is instanciated to take care of this
    model.  Otherwise, the user may create a repository inherited from
    this class.

    """

    def __init__(self, data_connector, model):
        """Default constructor.

        If an user redefines this method, she shouldn't forget the
        parameters:
            data_connector -- the data connector
            model -- the model (model.Model class)

        """
        self.data_connector = data_connector
        self.model = model

    def get_all(self):
        """Return all model objects."""
        with self.data_connector.u_lock:
            return self.data_connector.get_all_objects(self.model)

    def find(self, pkey=None, **kwargs):
        """Find and return (if found) an object identified by its keys.

        The positional argument, if set, represents the only primary
        key for this object.  This syntax is only allowed if the defined
        model has ONLY ONE primary key.  For instance, by default, it
        has one primary key:  the id.  The syntax:
        >>> repository.find(5)
        would be equivalent to:
        >>> repository.find(id=5)
        The fist syntax, though, is accepted if the model defines only
        one primary key.  Otherwise, the specified matching values could
        be specified as named arguments:
        >>> model.find(ref='AIX032', year=2012)

        You cannot use the 'find' method to search for an object via
        non-primary key fields.  To do this, you need a query.

        """
        model_name = get_name(self.model)
        pkey_names = get_pkey_names(self.model)
        pkey_values = OrderedDict()
        repr_pkey_names = tuple(repr(name) for name in pkey_names)
        if pkey:
            if len(pkey_names) != 1:
                raise ValueError("find method called with one positional " \
                        "argument whereas {} named arguments should be " \
                        "specified: {}".format(len(pkey_names),
                        ", ".join(repr_pkey_names)))

            pkey_values[pkey_names[0]] = pkey
        else:
            for name, value in kwargs.items():
                if name not in pkey_names:
                    raise ValueError("the field name {} is not a primary " \
                            "key field of the model {}".format(
                            repr(name), model_name))

                pkey_values[name] = value

            if len(pkey_values) != len(pkey_names):
                raise ValueError("not all primary key fields were " \
                        "specified for the model {}, expects {}".format(
                        model_name, ", ".join(repr_pkey_names)))

        object = None
        with self.data_connector.u_lock:
            object = self.data_connector.find_object(self.model, pkey_values)

        return object

    def create(self, **kwargs):
        """Create a new model object (model.Model instance) and save it.

        This method should create the new model's representation and
        save it in the data connector.

        """
        model_object = self.model(**kwargs)
        with self.data_connector.u_lock:
            self.data_connector.add_object(model_object)

    def update(self, model_object, attr, old_value):
        """Update the object in the data connector."""
        with self.data_connector.u_lock:
            self.data_connector.update_object(model_object, attr, old_value)

    def delete_(self, model_object):
        """Delete the object in the data connector."""
        with self.data_connector.u_lock:
            self.data_connector.remove_object(model_object)
