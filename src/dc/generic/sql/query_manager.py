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


"""Module defining the SqLQueryManager class, defined below."""

from abc import *

from dc.query_manager import QueryManager
from model.functions import *

class SQLQueryManager(QueryManager):

    """Generic class for the query manager using sQL queries.

    This class is supposed to deal with generic queries and convert them in
    SQL queries, supported by MOST of the potential SQL drivers.  Note,
    however, that all SQL libraries do not support each functionalities
    (or suport them the same way).  Therefore, this class should
    be inherited to integrate specific behaviors.

    """

    def query(self, query):
        """Look for the specified objects."""
        model = query.first_model
        plural_name = get_plural_name(model)
        table = self.driver.tables[plural_name]
        fields = table.fields
        statement = "SELECT * FROM {}".format(plural_name)
        if query.filters:
            statement += " WHERE "

        values = []
        list_formats = self.driver.generate_formats(
                sum(len(filter.parameters) for filter in query.filters))
        j = 0
        for i, filter in enumerate(query.filters):
            formats = []
            for parameter in filter.parameters:
                formats.append(list_formats[j])
                j += 1

            if i != 0:
                connector = query.connectors[i - 1]
                statement += " " + connector.upper() + " "

            statement += self.get_statement_from_filter(filter, formats)
            values.extend(filter.parameters)

        print("Statement", statement, values)
        lines = self.driver.execute_query(statement, *values)
        dict_lines = []
        for line in lines:
            dict_line = {}
            for i, field_name in enumerate(fields):
                value = line[i]
                dict_line[field_name] = value
            dict_lines.append(dict_line)

        return dict_lines

    def get_statement_from_filter(self, filter, formats):
        """Return the corresponding statement."""
        operator = filter.operator.name
        methods = {
                "=": self.op_equal,
                "!=": self.op_notequal,
        }

        return methods[operator](filter, formats)

    def op_equal(self, filter, formats):
        """Return the statement corresponding to the equal (=) operator."""
        return filter.field + "=" + formats[0]

    def op_notequal(self, filter, formats):
        """Return the statement corresponding to the notequal (!=) operator."""
        return filter.field + "!=" + formats[0]
