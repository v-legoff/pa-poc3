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


"""Module defining the PostgreSQLDriver class."""

import os

driver = True

try:
    import postgresql
except ImportError:
    driver = False

from dc.generic.sql.driver import SQLDriver
from dc import exceptions

class PostgreSQLDriver(SQLDriver):

    """Driver for PostgreSQL.

    As any driver, this one is only responsible for the communication
    between the Python Aboard's data layer (not the model's one) and
    the data storage (one PostgreSQL database with several tables
    in it).

    """

    SQL_TYPES = {
        "integer": "numeric",
        "string": "text",
    }

    def __init__(self):
        SQLDriver.__init__(self)
        self.format = "${}"

    def can_run(self):
        """Return whether the postgresql driver can run."""
        return driver

    def open(self, configuration):
        """Open the connexion."""
        host = configuration["host"]
        port = configuration["port"]
        dbuser = configuration["dbuser"]
        dbpass = configuration["dbpass"]
        dbname = configuration["dbname"]
        self.connection = postgresql.open(
                "pq://{user}:{password}@{host}:{port}/{database}".format(
                user=dbuser, password=dbpass, host=host, port=port,
                database=dbname))
        SQLDriver.open(self, configuration)

    def destroy(self):
        """Erase EVERY stored data."""
        self.clear()
        self.connection.close()

    def check_existing_tables(self):
        """Get the created tables."""
        query = "SELECT table_name FROM information_schema.tables"
        statement = self.connection.prepare(query)
        for row in statement():
            name = row[0]
            self.tables[name] = None

    def instruction_create_field(self, field_name, constraint):
        """Return the instruction used to create a simple field."""
        sql_field = type(self).SQL_TYPES[constraint.name_type]
        if constraint.has("auto_increment"):
            sql_field = "SERIAL"
        if constraint.has("pkey"):
            sql_field += " PRIMARY KEY"
        instruction = field_name + " " + sql_field
        return instruction

    def execute_query(self, statement, *args, many=True):
        """Execute a query and return the answer, if any."""
        preparation = self.connection.prepare(statement)
        if many:
            return preparation(*args)
        else:
            result = preparation(*args)
            if len(result) > 0:
                return result[0]

            return None

    def save(self):
        """Force the database saving."""
        pass
