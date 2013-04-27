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


"""This file contains the Driver class, described below."""

from abc import *
from threading import RLock

from dc.converters import *
from dc.exceptions import *

class Driver(metaclass=ABCMeta):

    """Class representing a driver for a specific data connector.

    A driver is used to communicate with the data connector (for instance,
    it manages the database connexion, if a database is used).  Drivers are
    not responsible of objects (they don't use Models at all) but they are
    used to store and retrieve datas using generic methods.  These methods
    are described in this class.

    """

    converters = {
        "list": ListConverter,
    }

    def line_to_storage(self, name, line):
        """Return a dictionary representing the line to save.

        This method uses the 'converters' class attribute which contains
        a dictionary with, in key, the field name (Integer, String,
        List, ...) and as values their corresponding formatters.  A
        formatter can be specific to a data connector or common to all
        data connectors.  If the field type is not in the 'converters'
        dictionary (or if its value is None), then no converter is used.

        To learn more about converters, look at the abstract class Converter
        in the converters/base.py file.

        """
        # First we get the table's field
        table = self.tables[name]
        fields = table.fields
        values = {}
        for name, constraint in fields.items():
            if name not in line:
                continue

            value = line[name]
            type_field = constraint.name_type
            if type(self).converters.get(type_field):
                converter = type(self).converters[type_field]
                value = converter.to_storage(value)

            values[name] = value

        return values

    @classmethod
    def value_to_storage(self, name, field_name, value):
        """Return a converted attribute."""
        table = self.tables[name]
        type_field = table.fields[field_name].type_name
        if cls.converters.get(type_field):
            converter = cls.converters[type_field]
            value = converter.to_storage(value)

        return value

    def storage_to_line(self, table_name, line):
        """Return the converted line of data."""
        # First we get the table's field
        table = self.tables[table_name]
        fields = table.fields
        values = {}
        for name, constraint in fields.items():
            value = line[name]
            type_field = constraint.name_type
            if type(self).converters.get(type_field):
                converter = type(self).converters[type_field]
                value = converter.to_object(value)

            values[name] = value

        return values


    def __init__(self):
        """Initialize the data connector."""
        # Locks for threads
        self.u_lock = RLock()
        self.running = False
        self.tables = {}

    @abstractmethod
    def can_run(self):
        """Return whether the driver can run or not.

        The driver wouldn't be able to run, for instance, if some specific
        library is needed (that's the case, most of the time).

        """
        pass

    @abstractmethod
    def open(self, configuration):
        """Open the Driver.

        This method is used to open a new connexion.  A driver is not made
        to manage several connexions, therefore it will raise an error if
        the connexion is already established.

        The configuration is a Configuration object that stores the selected
        (or default) configuration for the whole data connector.  Usually,
        this configuration contains different informations to open a
        connexion (for instance, the username and password for a PostgreSqL
        connexion).

        """
        if self.running:
            raise ConnexionAlreadyOpen("the connexion was open before")

        self.running = True

    @abstractmethod
    def close(self):
        """Close the connexion."""
        self.running = False

    @abstractmethod
    def clear(self):
        """Clear (delete) all datas."""
        pass

    def destroy(self):
        """Destroy alL the stored datas."""
        self.clear()
        self.close()

    @abstractmethod
    def add_table(self, table):
        """Add a new table to the driver, if it doesn't exist.

        NOTE: a table is not a model.  Most of the time, a table is the
        representation of a selected model but it's not always the case.  A
        table is a dc.table.Table object used to represent a document.  Some
        data storage (the MongoDB database, for instance) don't need these
        informations, but they are stored anyway because the model's system
        requires something with more constraints.

        """
        self.tables[table.name] = table

    @abstractmethod
    def query_for_lines(self, table_name):
        """Return all the table's line.

        This method should query for the specified table and return each
        line in a list of dictionary.

        """
        return []

    @abstractmethod
    def query_for_line(self, table_name, identifeirs):
        """Query for the specified line.

        This method should select and return the selected line, if found,
        or None if not.

        """
        pass

    @abstractmethod
    def add_line(self, table_name, line):
        """Add a new line to the table.

        Required arguments:
            table_name -- the table name, as used for 'add_table'
            line -- a dictionary containing the new line.
            auto_increments -- a list of the auto increment field names

        A line can be compared to a model object.  But the real process is:
        -   The RepositoryManager is asked to create a new object
        -   The object is created, the values are checked
        -   The repository manager asks the Driver to save this object (line).

        """
        pass

    @abstractmethod
    def update_line(self, table_name, identifiers, element, value):
        """Update an existing table line.

        Required arguments:
            table_name -- the table name, as used for 'add_table'
            identifiers -- the used identifiers (as a dictionary)
            element -- the element's name (a table field)
            value -- the new value

        The identifiers must be a dictionary of 'element: value' to get
        the correct line.  This values are not checked:  this is the
        role of the RepositoryManager to update the cache and check
        that this modification is possible.

        For instance, here's a standard call:
            update_line("users", {"id": 5}, "username", "Nother")

        """
        pass

    @abstractmethod
    def remove_line(self, table_name, identifiers):
        """Delete a line.

        The identifiers is a dictionary containing the '{element: value}'
        informations to get the proper line.  Once more, those values
        are not checked before deletion.

        """
        pass
