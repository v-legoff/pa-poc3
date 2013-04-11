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

    def filter(self, expression, parameter):
        """Try to create a new filter based on the expression.

        The expression musst be a string with one of the following structure:
            "field_name operator ?"
            "? operator field_name"

        The question mark (?) is replaced by the value of the
        parameter.  Here are some possible calls to this method:
            query.filter("username = ?", username)
            query.filter("email_address =", email)
            query.filter("? in tags", list_of_tags)

        """
        filter = Filter(expression, parameter)
        self.filters.append(filter)

    def execute(self):
        """Execute the query."""
        return self.data_connector.query(self)
