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


"""Module containing the Query class, described below."""

from model.functions import *
from query.filter import Filter

class Query:

    """Class representing a generic query with filters and specifications.

    This class provides several generic methods to build and extend
    a query.  When a query is created, it must find the used data
    connector.  When a query is executed, the whole query is sent to
    the data connector that should answer by a generic result, as well.

    """

    def __init__(self, data_connector, first_model=None):
        self.data_connector = data_connector
        self.first_model = first_model
        self.filters = []
        self.connectors = []

    def __str__(self):
        query = "select {}".format(get_name(self.first_model, bundle=True))
        if len(self.filters) == 1:
            query += " where " + str(self.filters[0])
        elif len(self.filters) > 1:
            query += " where " + str(self.filters[0])
            for connector, filter in zip(self.connectors, self.filters[1:]):
                query += " " + connector
                query += " " + str(filter)

        return query

    def filter(self, expression, *parameters, connector="and"):
        """Try to create a new filter based on the expression.

        The expression musst be a string with a structure defined by one
        of the operators.  The required parameters must be specified as
        question marks ('?') in the string and be present in the right
        order in the list of specified parameters.  Depending on the
        operator, one or more parameters may be expected.

        This example uses the '=' operator.  The 'username'
        variable contains a string:
            filter("username = ?", username)

        """
        filter = Filter(expression, *parameters)
        self.filters.append(filter)
        connector = connector.lower()
        if connector not in ("and", "or"):
            raise ValueError("unknown connector {}".format(repr(connector)))

        self.connectors.append(connector)

    def execute(self, many=True):
        """Execute the query."""
        result = self.data_connector.query_manager.query_objects(self)
        if many:
            return result

        if isinstance(result, list):
            return result[0]

        return None
