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


"""This module contains the Table class.

This class is used to represent a generic table for the data connectors.
The meaning is very close to a "table" in *SQL models, even if it has to
be interpreted by no-SQL models, as well.

A Table IS NOT a model.  It contains a name and an ordered dictionary
containing fields:  the name of the field is the key and a constraint is
the corresponding value.

NOTE: a table is often used to represent a Model class, but a table
is built in the repository manager of the specific data connector.  A
table is not data connector-specific.

"""

from collections import OrderedDict

class Table:

    """Class representing a Table object.

    It contains:
        name -- the table's name
        fields -- the table's fields as a ordered dictionary.

    The keys and values of this dictionary are the field's name and a
    constraint type.

    """

    def __init__(self, name):
        self.name = name
        self.fields = OrderedDict()

    def __repr__(self):
        ret = "<table {} (".format(self.name)
        first = True
        for name, constraint in self.fields.items():
            if not first:
                ret += "\n"

            ret += "  " + name
            if constraint:
                ret += ":" + str(constraint)

            first = False

        ret += ")>"
        return ret

    def add_field(self, name, constraint):
        """Create a new field.

        Expected arguments:
            name -- the field's name
            constraint -- the corresponding constraint.

        """
        self.fields[name] = constraint
