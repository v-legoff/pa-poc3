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


"""Module containing the class Schema detailed below."""

from configuration.data import Data
from configuration.exceptions import *

class Schema:

    """Class defining a configuration schema.

    A schema is a dictionary of at least one dimension that contains,
    as keys, the data names and as values, Data object.  Schemas are
    used to define the structure of a configuration object (such as
    a configuration file).  Here's an example of the definition of a
    schema:
        schema = Schema("schema", definition={
                "host": Data("the server's host", default="127.0.0.1"),
                "port": Data("the server's port", type=int, default=9000),
        })

    You can also use, as values:
        Another Schema object
        A callable that will be called to determine the value

    """

    def __init__(self, name, definition=None):
        """Create a new schema.

        The definition, if specified, must be a dictionary.

        """
        definition = definition or {}
        self.name = name
        self.definition = definition

    def __repr__(self):
        return "<schema with definition {}>".format(
                repr(self.definition))

    def validate(self, configuration, parent=None):
        """Try to validate the specified configuration.

        This configuration must be a dictionary and will be confronted
        to the schema.

        A configuration is validated in a specific order:
            First are validated all datas that contain Data objects
            Next are validated those containing Schema objects
            Finally the one with callbacks are validated

        """
        if not isinstance(configuration, dict):
            raise BadDataType("the schema {} expects a dictionary, got {} " \
                    "({})".format(repr(self.name), repr(configuration),
                    type(configuration)))

        simple_datas = [name for name, value in self.definition.items() if \
                isinstance(value, Data)]
        other_schemas = [name for name, value in self.definition.items() if \
                isinstance(value, Schema)]
        callables = [name for name, value in self.definition.items() if \
                callable(value)]

        # Use the 'handle_special_chars' static method
        self.handle_special_chars(simple_datas, other_schemas, callables,
                configuration)

        # First validate the simple datas
        for name in simple_datas:
            data = self.definition[name]
            data.name = self.name + "[" + name + "]"
            value = configuration.get(name)
            value = data.validate(value)
            configuration[name] = value

        # Then validate the ssub-schemas
        for name in other_schemas:
            schema = self.definition[name]
            schema.name = name + "." + schema.name
            value = configuration.get(name, {})
            value = schema.validate(value)
            configuration[name] = value

        # Finally, validate the callables
        for name in callables:
            function = self.definition[name]
            function(configuration)

        return configuration

    @staticmethod
    def handle_special_chars(datas, schemas, callables, schema):
        """Handle the special characters like '*'.

        Some special characters may be used in a schema definition:
            The '*' means all other non-handled configuration

        """
        for i, name in enumerate(list(schemas)):
            if name == "*":
                others = list(schema.keys())
                others = [key for key in others if key not in \
                        datas and key not in schemas and key not in callables]
                schemas.extend(others)
