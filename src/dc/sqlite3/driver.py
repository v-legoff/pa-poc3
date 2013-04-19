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


"""Module defining the Sqlite3Driver class."""

import os

driver = True

try:
    import sqlite3
except ImportError:
    driver = False

from dc.driver import Driver
from dc import exceptions

TYPES = {
    "integer": "integer",
    "string": "text",
}

class Sqlite3Driver(Driver):

    """Driver for sqlite3.

    As any driver, this one is only responsible for the communication
    between the Python Aboard's data layer (not the model's one) and
    the data storage (one sqlite database, as a file, with several tables
    inside it).

    """

    def __init__(self):
        Driver.__init__(self)
        self.location = None
        self.existing_tables = {}

    def can_run(self):
        """Return whether the sqlite3 driver can run."""
        return driver

    def open(self, configuration):
        """Open the connexion."""
        Driver.open(self, configuration)
        location = configuration["location"]
        location = location.replace("\\", "/")
        if location.startswith("~"):
            location = os.path.expanduser("~") + location[1:]
        parent = os.path.dirname(location)
        if not os.path.exists(parent):
            os.makedirs(parent)

        if not os.access(parent, os.R_OK):
            raise exceptions.DriverInitializationError(
                    "cannot read in {}".format(parent))
        if not os.access(parent, os.W_OK):
            raise exceptions.DriverInitializationError(
                    "cannot write in {}".format(parent))

        self.location = location
        self.connection = sqlite3.connect(self.location)
        self.check_existing_tables()

    def close(self):
        """Close the data connector (nothing to be done)."""
        Driver.close(self)
        self.connection.close()

    def clear(self):
        """Clear (delete) the stored datas."""
        pass
        #self.connection.commit()
        #cursor = self.connection.cursor()
        #for table in self.tables:
        #    cursor.execute("DROP TABLE {}".format(table))

    def destroy(self):
        """Erase EVERY stored data."""
        self.connection.close()
        os.remove(self.location)

    def check_existing_tables(self):
        """Get the created tables."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        for name in tables:
            self.existing_tables[name] = None

    def add_table(self, table):
        """Add the new table if it doesn't exist."""
        Driver.add_table(self, table)
        name = table.name
        if name not in self.existing_tables:
            self.existing_tables[name] = table
            fields = table.fields
            sql_fields = []
            for field_name, constraint in fields.items():
                sql_field = TYPES[constraint.name_type]
                instruction = field_name + " " + sql_field
                if constraint.has("pkey"):
                    instruction += " PRIMARY KEY"
                if constraint.has("auto_increment"):
                    instruction += " AUTOINCREMENT"
                sql_fields.append(instruction)

            query = "CREATE TABLE {} ({})".format(name, ", ".join(sql_fields))
            cursor = self.connection.cursor()
            cursor.execute(query)

    def read_table(self, name, file):
        """Read a whole table contained in a file.

        This file is supposed to be formatted as a YAML file.  Furthermore,
        the 'yaml.load' function should return a list of dictionaries.

        The first dictionary describes some table informations, as
        the status of the autoincrement fields.  Each following dictionary
        is a line of data which sould describe a model object.

        """
        content = file.read()
        datas = yaml.load(content)
        if not isinstance(datas, list):
            raise exceptions.DataFormattingError(
                    "the file {} must contain a YAML formatted list".format(
                    self.files[name]))

        table_datas = datas[0]
        if not isinstance(table_datas, dict):
            raise exceptions.DataFormattingError(
                    "the table informations are not stored in a YAML " \
                    "dictionary in the file {}".format(self.files[name]))

        self.read_table_header(name, table_datas)
        return datas[1:]

    def query_for_lines(self, table_name):
        """Return all the table's line.

        This method should query for the specified table and return each
        line in a list of dictionary.

        """
        table = self.tables[table_name]
        query = "SELECT * FROM " + table_name
        cursor = self.connection.cursor()
        cursor.execute(query)
        lines = []
        for row in cursor.fetchall():
            line = {}
            for i, field_name in enumerate(table.fields.keys()):
                line[field_name] = row[i]

            lines.append(line)

        return lines

    def query_for_line(self, table_name, identifiers):
        """Query for the specified line.

        This method should select and return the selected line, if found,
        or None if not.

        """
        table = self.tables[table_name]
        query = "SELECT * FROM {} WHERE ".format(table_name)
        params = []
        filters = []
        for name, value in identifiers.items():
            filters.append("{}=?".format(name))
            params.append(value)

        query += " AND ".join(filters)
        cursor = self.connection.cursor()
        cursor.execute(query, tuple(params))
        row = cursor.fetchone()
        if row is None:
            return None

        line = {}
        for i, field_name in enumerate(table.fields.keys()):
            line[field_name] = row[i]

        return line

    def add_line(self, table_name, line):
        """Add a new line."""
        table = self.tables[table_name]
        ret = {}
        query = "INSERT INTO " + table_name + " ("
        names = []
        values = []
        auto_increments = []
        for field_name, constraint in table.fields.items():
            if constraint.has("auto_increment"):
                auto_increments.append(field_name)
                continue

            names.append(field_name)
            values.append(line[field_name])

        query += ", ".join(names) + ") values("
        query += ", ".join("?" * len(values)) + ")"
        cursor = self.connection.cursor()
        cursor.execute(query, tuple(values))

        for field in auto_increments:
            query = "SELECT max(" + field + ") FROM " + table_name
            cursor.execute(query)
            row = cursor.fetchone()
            value = row[0]
            ret[field] = value

        self.connection.commit()
        return ret

    def update_line(self, table_name, identifiers, element, value):
        """Update a line (does nothing)."""
        params = [value]
        params.extend(identifiers.values())
        names = [name + "=?" for name in identifiers]
        query = "UPDATE " + table_name + " SET " + element + "=?"
        query += " WHERE " + " AND ".join(names)
        cursor = self.connection.cursor()
        cursor.execute(query, tuple(params))
        self.connection.commit()

    def remove_line(self, table_name, identifiers):
        """Delete the line (do nothing)."""
        names = tuple(name + "=?" for name in identifiers.keys())
        values = tuple(identifiers.values())
        query = "DELETE FROM " + table_name
        query += " WHERE " + " AND ".join(names)
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
