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


"""Module defining the YAMLDriver class."""

import os

driver = True

try:
    import yaml
except ImportError:
    driver = False

from dc.driver import Driver
from dc import exceptions

class YAMLDriver(Driver):

    """Driver for YAML.

    As any driver, this one is only responsible for the communication
    between the Python Aboard's data layer (not the model's one) and
    the data storage (several YAML files, here).

    """

    def __init__(self):
        Driver.__init__(self)
        self.location = None
        self.auto_increments = {}
        self.to_update = set()

    def can_run(self):
        """Return whether the YAML driver can run."""
        return driver

    def open(self, configuration):
        """Open the connexion."""
        Driver.open(self, configuration)
        location = configuration["location"]
        location = location.replace("\\", "/")
        if location.startswith("~"):
            location = os.path.expanduser("~") + location[1:]

        if location.endswith("/"):
            location = location[:-1]

        if not os.path.exists(location):
            # Try to create it
            os.makedirs(location)

        if not os.access(location, os.R_OK):
            raise exceptions.DriverInitializationError(
                    "cannot read in {}".format(location))
        if not os.access(location, os.W_OK):
            raise exceptions.DriverInitializationError(
                    "cannot write in {}".format(location))

        self.location = location
        self.files = {}

    def close(self):
        """Close the data connector (nothing to be done)."""
        Driver.close(self)

    def clear(self):
        """Clear (delete) the stored datas."""
        pass

    def destroy(self):
        """Erase EVERY stored data."""
        for file in os.listdir(self.location):
            os.remove(self.location + "/" + file)

    def add_table(self, table):
        """Add the new table if it doesn't exist."""
        Driver.add_table(self, table)
        name = table.name
        filename = self.location + "/" + name + ".yml"
        self.files[name] = filename
        if os.path.exists(filename):
            with open(filename, "r") as file:
                return self.read_table(name, file)

        return []

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

    def read_table_header(self, name, datas):
        """Read the table header.

        This header should describe some informations concerning the
        table (as the autoincrement fields).

        """
        auto_increments = datas.get("auto_increments", {})
        self.auto_increments[name] = auto_increments

    def write_table(self, name, lines):
        """Write the table in a file."""
        # First, we get the header
        header = {}
        if name in self.auto_increments:
            header["auto_increments"] = self.auto_increments[name]

        # Then save the lines
        lines.insert(0, header)
        content = yaml.dump(lines, default_flow_style=False)
        with open(self.location + "/" + name + ".yml", "w") as file:
            file.write(content)

    def add_line(self, table_name, line):
        """Add a new line."""
        table = self.tables[table_name]
        ret = {}
        auto_increments = [name for name, constraint in \
                table.fields.items() if constraint and constraint.has(
                "auto_increment")]
        auto_increments_def = self.auto_increments.get(table_name, {})
        if auto_increments:
            self.auto_increments[table_name] = {}

        for field_name in auto_increments:
            value = auto_increments_def.get(field_name, 1)
            ret[field_name] = value
            self.auto_increments[table_name][field_name] = value + 1

        self.to_update.add(table_name)
        return ret

    def update_line(self, table_name, identifiers, element, value):
        """Update a line (does nothing)."""
        pass

    def remove_line(self, table_name, identifiers):
        """Delete the line (do nothing)."""
        pass
