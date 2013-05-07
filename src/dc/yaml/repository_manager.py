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


"""Module defining the YAMLRepositoryManager class."""

from dc.repository_manager import RepositoryManager
from dc import exceptions
from model import exceptions as mod_exceptions
from model.functions import *

class YAMLRepositoryManager(RepositoryManager):

    """Repository manager for YAML."""


    def record_model(self, model):
        """Record the given model."""
        RepositoryManager.record_model(self, model)
        name = get_name(model)
        table = self.build_table(model)
        lines = self.driver.add_table(table)
        for line in lines:
            model_object = self.storage_to_object(name, line)
            self.cache_object(model_object)

    def save(self):
        """Write the YAML files."""
        names = {}
        for name, model in self.models.items():
            plural_name = get_plural_name(model)
            names[plural_name] = name

        for table in self.driver.to_update:
            name = names[table]
            lines = []
            for object in self.objects_tree[name].values():
                lines.append(self.object_to_storage(object))

            self.driver.write_table(table, lines)

        self.driver.to_update.clear()

    def get_all_objects(self, model):
        """Return all the model's object in a list."""
        name = get_name(model)
        return list(self.objects_tree.get(name, {}).values())

    def find_matching_objects(self, field, value):
        """Return the matching models.

        This method is used to retrieve the matching models of a
        related field.

        """
        model = field.model
        name = get_name(model)
        field_name = field.field_name
        objects = [model_object for model_object in self.objects_tree[ \
                name].values() if getattr(model_object, field_name) == value]
        return objects

    def add_object(self, model_object):
        """Save the object, issued from a model."""
        RepositoryManager.add_object(self, model_object)

    def update_object(self, model_object, attribute, old_value):
        """Update an object."""
        RepositoryManager.update_object(self, model_object, attribute,
                old_value)

    def remove_object(self, model_object):
        """Delete the object."""
        RepositoryManager.remove_object(self, model_object)
