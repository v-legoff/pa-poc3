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

from dc.generic.sql.driver import SQLDriver
from dc import exceptions

class Sqlite3Driver(SQLDriver):

    """Driver for sqlite3.

    As any driver, this one is only responsible for the communication
    between the Python Aboard's data layer (not the model's one) and
    the data storage (one sqlite database, as a file, with several tables
    inside it).

    """

    SQL_TYPES = {
        "integer": "integer",
        "string": "text",
    }

    def __init__(self):
        SQLDriver.__init__(self)
        self.location = None

    def can_run(self):
        """Return whether the sqlite3 driver can run."""
        return driver

    def open(self, configuration):
        """Open the connexion."""
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
        SQLDriver.open(self, configuration)

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
            self.tables[name] = None
