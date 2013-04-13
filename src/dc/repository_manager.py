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


"""This file contains the RepositoryManager class, described below."""

from abc import *

from dc.table import Table
from model import exceptions as mod_exceptions
from model.functions import *
from model.types import *

class RepositoryManager(metaclass=ABCMeta):

    """Class representing a data connector repository manager.

    This class uses the Model objects to communicate with the drivers.  It
    is also responsible of the cache.

    """

    def __init__(self, driver):
        self.driver = driver
        self.objects_tree = {}
        self.models = {}
        self.deleted_objects = []

    def clear(self):
        """Clear the stored datas and the cache."""
        self.driver.clear()
        self.objects_tree = {}
        self.record_models(list(self.models.values()))

    def record_models(self, models):
        """Record the given models.

        The parameter must be a list of classes.  Each class must
        be a model.

        """
        for model in models:
            self.record_model(model)

    def record_model(self, model):
        """Record the given model, a subclass of model.Model."""
        name = get_name(model)
        self.models[name] = model
        self.objects_tree[name] = {}

    def save(self):
        """Force the data connector to save."""
        pass

    @abstractmethod
    def get_all_objects(self, model):
        """Return all the model's object in a list."""
        pass

    @abstractmethod
    def find_object(self, model, pkey_values):
        """Return, if found, the selected object.

        Raise a model.exceptions.ObjectNotFound if not found.

        """
        pass

    @abstractmethod
    def add_object(self, model_object):
        """Save the object, issued from a model.

        Usually this method should:
        -   Save the object (in a database, for instance)
        -   Cache the object.

        """
        plural_name = get_plural_name(type(model_object))
        to_store = self.object_to_storage(model_object)
        name = get_plural_name(type(model_object))
        other_fields = self.driver.add_line(plural_name, to_store)
        for field_name, value in other_fields.items():
            object.__setattr__(model_object, field_name, value)

        self.cache_object(model_object)

    @abstractmethod
    def update_object(self, model_object, attribute, old_value):
        """Update an object."""
        self.check_update(model_object)
        field = getattr(type(model_object), attribute)
        value = getattr(model_object, attribute)
        identifiers = get_pkey_values(model_object, {attribute: old_value})
        name = get_plural_name(type(model_object))
        self.driver.update_line(name, identifiers, attribute, value)
        self.update_cache(model_object, field, old_value)

    def remove_object(self, model_object):
        """Delete object from cache."""
        name = get_plural_name(type(model_object))
        identifiers = get_pkey_values(model_object)
        self.driver.remove_line(name, identifiers)
        self.uncache_object(model_object)

    def get_from_cache(self, model, attributes):
        """Return, if found, the cached object.

        The expected parameters are:
            model -- the model (Model subclass)
            attributes -- a dictionary {name1: value1, ...}

        """
        name = get_name(model)
        pkey_names = get_pkey_names(model)
        cache = self.objects_tree.get(name, {})
        values = tuple(attributes.get(name) for name in pkey_names)
        if len(values) == 1:
            values = values[0]

        return cache.get(values)

    def cache_object(self, object):
        """Save the object in cache."""
        pkey = get_pkey_values(object)
        if len(pkey) == 1:
            pkey = pkey[0]

        self.objects_tree[get_name(type(object))][pkey] = object

    def uncache_object(self, object):
        """Remove the object from cache."""
        name = get_name(type(object))
        values = tuple(get_pkey_values(object))
        if len(values) == 1:
            values = values[0]

        cache = self.objects_tree.get(name, {})
        if values in cache.keys():
            del cache[values]
            self.deleted_objects.append((name, values))

    def update_cache(self, object, field, old_value):
        """This method is called to update the cache for an object.

        If the field is one of the primary keys, then it should be
        updated in the cache too.

        """
        attr = field.field_name
        if old_value is None:
            return

        if not field.has_constraint("pkey"):
            return

        pkey = get_pkey_values(object)
        old_pkey = get_pkey_values(object, {attr: old_value})

        if len(pkey) == 1:
            pkey = pkey[0]
            old_pkey = old_pkey[0]

        name = get_name(type(object))
        tree = self.objects_tree[name]
        if old_pkey in tree:
            del tree[old_pkey]
        tree[pkey] = object

    def clear_cache(self):
        """Clear the cache."""
        self.objects_tree = {}

    def check_update(self, model_object):
        """Raise a ValueError if the object was deleted."""
        if self.was_deleted(model_object):
            raise mod_exceptions.UpdateDeletedObject(model_object)

    def was_deleted(self, model_object):
        """Return whether the object was deleted (uncached)."""
        name = get_name(type(model_object))
        values = tuple(get_pkey_values(model_object))
        if len(values) == 1:
            values = values[0]

        return (name, values) in self.deleted_objects

    def object_to_storage(self, model_object):
        """Return a dictionary containing the model object's fields values."""
        plural_name = get_plural_name(type(model_object))
        fields = get_fields(type(model_object), register=True)
        values = {}
        for field in fields:
            value = getattr(model_object, field.field_name)
            values[field.field_name] = value

        return self.driver.line_to_storage(plural_name, values)

    def storage_to_object(self, name, line):
        """Return a Model object based on the dictionary."""
        model = self.models[name]
        plural_name = get_plural_name(model)
        line = self.driver.storage_to_line(plural_name, line)
        model_object = model(**line)
        return model_object

    def build_table(self, model):
        """Build a table on a model object."""
        name = get_plural_name(model)
        table = Table(name)
        fields = get_fields(model, register=True)
        for field in fields:
            table.add_field(field.field_name, field.constraint)

        return table
