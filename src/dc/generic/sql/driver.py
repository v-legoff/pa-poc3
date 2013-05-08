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


"""Module defining the SQLDriver class."""

from abc import *

from dc.driver import Driver
from dc import exceptions

class SQLDriver(Driver):

    """Generic driver for sending SQL queries."""

    SQL_TYPES = {}

    def __init__(self):
        Driver.__init__(self)
        self.format = "?"
        self.tables = {}
        self.connection = None

    def generate_formats(self, nb):
        """Generate a tuple of formatted values.

        The format is a string containing something like "?" or "*{}".
        If the second is choosen, different formats are used, depending
        on the given number.  For instance, if the format is "${}" and
        we call 'generate_format' with the parameter at 5, we should
        obtain ("$1", "$2", "$3", "$4", "$5").

        """
        formats = []
        for i in range(nb):
            formats.append(self.format.format(i + 1))

        return formats

    def open(self, configuration):
        """Open the connection.

        The connection must be set up in the 'connection' instance
        attribute.  While redefining this method, you MUST call the
        parent AFTER setting up the connection.

        """
        Driver.open(self, configuration)
        self.check_existing_tables()

    def close(self):
        """Close the data connector (simply close the conection)."""
        Driver.close(self)
        self.connection.close()

    def clear(self):
        """Clear (delete) the stored datas."""
        for name, table in self.tables.items():
            if table is not None:
                self.execute_query("DROP TABLE {}".format(name))
        self.tables = {}

    def destroy(self):
        """Erase EVERY stored data."""
        self.connection.close()

    @abstractmethod
    def check_existing_tables(self):
        """Get the created tables."""
        pass

    @abstractmethod
    def execute_query(self, statement, *args, many=True):
        """Execute a query and return the answer, if any.

        This method mst be redefined by redefined by the definitive driver.

        """
        pass

    def add_table(self, table):
        """Add the new table if it doesn't exist."""
        name = table.name
        existing_tables = list(self.tables.keys())
        Driver.add_table(self, table)
        self.tables[name] = table
        if name not in existing_tables:
            fields = table.fields
            sql_fields = []
            for field_name, constraint in fields.items():
                instruction = self.instruction_create_field(field_name,
                        constraint)
                sql_fields.append(instruction)

            query = "CREATE TABLE {} ({})".format(name, ", ".join(sql_fields))
            self.execute_query(query)

    def instruction_create_field(self, field_name, constraint):
        """Return the instruction used to create a simple field."""
        sql_field = type(self).SQL_TYPES[constraint.name_type]
        instruction = field_name + " " + sql_field
        if constraint.has("pkey"):
            instruction += " PRIMARY KEY"
        if constraint.has("auto_increment"):
            instruction += " AUTOINCREMENT"
        return instruction

    def query_for_lines(self, table_name):
        """Return all the table's line.

        This method should query for the specified table and return each
        line in a list of dictionary.

        """
        table = self.tables[table_name]
        query = "SELECT * FROM " + table_name
        rows = self.execute_query(query)
        lines = []
        for row in rows:
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
        formats = self.generate_formats(len(identifiers))
        for i, (name, value) in enumerate(identifiers.items()):
            format = formats[i]
            filters.append("{}={}".format(name, format))
            params.append(value)

        query += " AND ".join(filters)
        row = self.execute_query(query, *params, many=False)
        if row is None:
            return None

        line = {}
        for i, field_name in enumerate(table.fields.keys()):
            line[field_name] = row[i]

        return line

    def find_matching_lines(self, table_name, matches):
        """Return the matching list of lines.

        This method is used to fetch lines that have relations
        between them.  The matches are a dictionary containing the
        line's attributes that should match.

        """
        table = self.tables[table_name]
        query = "SELECT * FROM " + table_name
        formats = self.generate_formats(len(matches))
        if matches:
            query += " WHERE "

        lines = []
        for match, format in zip(matches, formats):
            lines.append(match + "=" + format)

        query += " AND ".join(lines)
        rows = self.execute_query(query, *matches.values())
        lines = []
        for row in rows:
            line = {}
            for i, field_name in enumerate(table.fields.keys()):
                line[field_name] = row[i]

            lines.append(line)

        return lines

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
        query += ", ".join(self.generate_formats(len(values))) + ")"
        self.execute_query(query, *values)

        for field in auto_increments:
            query = "SELECT max(" + field + ") FROM " + table_name
            row = self.execute_query(query, many=False)
            value = row[0]
            ret[field] = value

        self.save()
        return ret

    def update_line(self, table_name, identifiers, element, value):
        """Update a line (does nothing)."""
        params = [value]
        params.extend(identifiers.values())
        names = []
        formats = self.generate_formats(len(params))
        for i, name in enumerate(identifiers):
            format = formats[i + 1]
            names.append(name + "={}".format(format))

        query = "UPDATE " + table_name + " SET " + element + "=" + formats[0]
        query += " WHERE " + " AND ".join(names)
        self.execute_query(query, *params)
        self.save()

    def remove_line(self, table_name, identifiers):
        """Delete the line (do nothing)."""
        names = []
        formats = self.generate_formats(len(identifiers))
        for i, name in enumerate(identifiers):
            format = formats[i]
            names.append(name + "={}".format(format))

        values = tuple(identifiers.values())
        query = "DELETE FROM " + table_name
        query += " WHERE " + " AND ".join(names)
        self.execute_query(query, *values)
        self.save()
