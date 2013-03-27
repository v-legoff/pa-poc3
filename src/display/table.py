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


"""Module containing the Table class used to represent a table."""

from display.row import Row

class Table:

    """Class used to represent a table with specified columns.

    To build it, you have two options:
        Call the constructor with each column name as a positional argument
        Call the constructor and then use the 'add_column' method

    After setting up the right amount of columns you can use the
    'add_row' method.  This method will return a Row object (see the
    'display.row' module) and you will be able to add new informations
    in it.  Here is a sample of code using tables:
    >>> from display.table import Table
    >>> contacts = Table("First name", "Name", "job")
    >>> # Note that you can achive the same by doing for instance:
    >>> # contacts = Table("First name", "Name")
    >>> # contacts.add_column("job")
    >>> contacts.add_row("Mike", "Arthur", "developer")
    >>> row = contact.add_row("John", "Wingham")
    >>> row.set("job", "designer")
    >>> print(contacts)
    +------------+---------+-----------+
    | First name | Name    | Job       |
    +------------+---------+-----------+
    | Mike       | Arthur  | developer |
    | John       | Wingham | designer  |
    +------------+---------+-----------+

    Methods to sort and present the table are also provided.

    """
    def __init__(self, *columns, column_separator=" | ", left_border="| ",
                right_border=" |"):
        self.columns = list(columns)
        self.rows = []
        self.column_separator = column_separator
        self.left_border = left_border
        self.right_border = right_border

    def __repr__(self):
        return "<table of {} columns on {} rows".format(len(self.columns),
                len(self.rows))

    def __str__(self):
        return self.display()

    def add_column(self, name):
        """Add a new column."""
        self.columns.append(name)

    def add_row(self, *contents):
        """Add a new row with each column content as a positional argument.

        You can partly fill a row and then set new informations.  This
        method return the newly created row and you can manipulate
        it to update its content.

        """
        row = Row(self)
        row.set_contents(*contents)
        self.rows.append(row)
        return row

    def display(self):
        """Display the table."""
        column_sizes = []
        for column in self.columns:
            column_sizes.append(len(column))

        for row in self.rows:
            for i, column in enumerate(row):
                length = column_sizes[i]
                if length < len(column):
                    column_sizes[i] = len(column)
        length_line = sum(column_sizes) + len(self.column_separator) * \
                len(self.columns)
        length_line += len(self.left_border) + len(self.right_border)

        if length_line > 79:
            raise ValueError("line too long")

        lines = []
        line_format = self.left_border
        for i, size in enumerate(column_sizes):
            if i > 0:
                line_format += self.column_separator
            line_format += "{:<" + str(size) + "}"
        line_format += self.right_border
        lines.append(line_format.format(*self.columns))
        for row in self.rows:
            lines.append(line_format.format(*row.datas))

        return "\n".join(lines)
