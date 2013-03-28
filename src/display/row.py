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


"""Module containing the Row class, representing a table row."""

class Row:

    """Class representing a row table."""

    def __init__(self, table):
        self.table = table
        self.named_datas = {}

    def __iter__(self):
        return iter(self.datas)

    @property
    def datas(self):
        """Return the row in the right order."""
        datas = []
        for column in self.table.columns:
            data = self.named_datas.get(column, "")
            datas.append(data)

        return datas

    def get_tuple(self, *columns):
        """Return a tuple containing the required datas."""
        datas = []
        for name in columns:
            datas.append(self.named_datas.get(name, ""))

        return tuple(datas)

    def set(self, name, value):
        """Set the column."""
        if name not in self.table.columns:
            raise ValueError("the column's name {} doesn't exist in this " \
                    "table".format(name))

        self.named_datas[name] = value

    def set_contents(self, *contents):
        """Set multiple columns."""
        length = len(contents)
        if length > len(self.table.columns):
            raise ValueError("too many arguments for a {}-rows " \
                    "table".format(length))

        names = self.table.columns[:length]
        for i, name in enumerate(names):
            content = contents[i]
            self.named_datas[name] = content
