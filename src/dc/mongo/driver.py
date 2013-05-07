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


"""Module defining the MongoDriver class."""

driver = True

try:
    import pymongo
except ImportError:
    driver = False

from dc.driver import Driver
from dc import exceptions

class MongoDriver(Driver):

    """Driver for the 'mongo' data connector using pymongo.

    As any driver, this one is only responsible for the communication
    between the Python Aboard's data layer (not the model's one) and
    the data storage (a MongoDB connection).

    """

    def __init__(self):
        Driver.__init__(self)
        self.db_name = "datas"
        self.inc_name = "increments"
        self.connection = None
        self.datas = None
        self.increments = None
        self.collections = {}
        self.inc_collections = {}
        self.object_ids = {}

    def can_run(self):
        """Return whether the YAML driver can run."""
        return driver

    def open(self, configuration):
        """Open the connexion."""
        Driver.open(self, configuration)
        self.db_name = configuration["datas"]
        self.inc_name = configuration["increments"]

        # Try to connect
        self.connection = pymongo.Connection()

        # Create the datas and increments collections
        self.datas = self.connection[self.db_name]
        self.increments = self.connection[self.inc_name]

        # Set the collections
        self.collections = {}
        self.inc_collections = {}

        # Keep the IDs in cache
        self.line_ids = {}
        self.id_lines = {}

    def close(self):
        """Close the data connector (nothing to be done)."""
        Driver.close(self)
        self.connection.close()

    def clear(self):
        """Clear (delete) the stored datas."""
        for name in self.tables:
            self.datas[name].remove()
            self.datas.drop_collection(name)
            self.increments[name].remove({})
            self.increments.drop_collection(name)
        self.tables.clear()

    def destroy(self):
        """Erase EVERY stored data."""
        self.connection.drop_database(self.db_name)
        self.connection.drop_database(self.inc_name)
        self.connection.close()

    def add_table(self, table):
        """Add the new table."""
        Driver.add_table(self, table)
        name = table.name
        self.collections[name] = self.datas[name]
        self.inc_collections[name] = self.increments[name]
        self.line_ids[name] = {}

    def query_for_lines(self, table_name):
        """Return all the table's line.

        This method should query for the specified table and return each
        line in a list of dictionary.

        """
        table = self.tables[table_name]
        datas = self.datas[table_name].find()
        lines = []
        for data in datas:
            identifiers = {}
            for name, constraint in table.fields.items():
                if constraint.has("pkey"):
                    identifiers[name] = data[name]

            m_id = data["_id"]
            del data["_id"]
            self.line_ids[table_name][tuple(identifiers.items())] = m_id
            self.id_lines[m_id] = data
            lines.append(data)

        return lines

    def query_for_line(self, table_name, identifiers):
        """Query for the specified line.

        This method should select and return the selected line, if found,
        or None if not.

        """
        datas = self.datas[table_name].find_one(dict(identifiers))

        if datas:
            m_id = datas["_id"]
            del datas["_id"]
            self.line_ids[table_name][tuple(identifiers.items())] = m_id
            self.id_lines[m_id] = datas
            return datas

        return None

    def find_matching_lines(self, table_name, matches):
        """Return the matching list of lines.

        This method is used to fetch lines that have relations
        between them.  The matches are a dictionary containing the
        line's attributes that should match.

        """
        table = self.tables[table_name]
        datas = self.datas[table_name].find(matches)
        lines = []
        for data in datas:
            identifiers = {}
            for name, constraint in table.fields.items():
                if constraint.has("pkey"):
                    identifiers[name] = data[name]

            m_id = data["_id"]
            del data["_id"]
            self.line_ids[table_name][tuple(identifiers.items())] = m_id
            self.id_lines[m_id] = data
            lines.append(data)

        return lines

    def get_and_update_increment(self, table, field):
        """Get and update an auto-increment field.

        If not found in the specified table, return 1 but update to 2.

        """
        value = self.increments[table].find_one({"name": field})
        if value:
            value = value["current"]
        else:
            value = 1

        self.increments[table].remove({"name": field})
        self.increments[table].insert({
                "name": field,
                "current": value + 1,
        }, w=True)

        return value

    def add_line(self, table_name, line):
        """Add a new line."""
        table = self.tables[table_name]
        ret = {}
        auto_increments = [field_name for field_name, constraint in \
                table.fields.items() if constraint.has("auto_increment")]
        for field in auto_increments:
            ret[field] = self.get_and_update_increment(table_name, field)

        line.update(ret)
        m_id = self.datas[table_name].insert(line, w=True)
        identifiers = dict((field_name, line[field_name]) for \
                field_name, constraint in table.fields.items() if \
                constraint.has("pkey"))
        self.line_ids[table_name][tuple(identifiers.items())] = m_id
        self.id_lines[m_id] = line
        return ret

    def update_line(self, table_name, identifiers, element, value):
        """Update a line (does nothing)."""
        m_id = self.line_ids[table_name][tuple(identifiers.items())]
        all_line = self.id_lines[m_id]
        all_line.update({element: value})
        self.datas[table_name].update({"_id": m_id}, all_line)

    def remove_line(self, table_name, identifiers):
        """Delete the line (do nothing)."""
        m_id = self.line_ids[table_name][tuple(identifiers.items())]
        self.datas[table_name].remove(m_id, fsync=True)
        del self.line_ids[table_name][tuple(identifiers.items())]
        del self.id_lines[m_id]
