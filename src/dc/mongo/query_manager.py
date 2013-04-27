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


"""Module defining the MongoQueryManager class, defined below."""

from dc.query_manager import QueryManager
from model.functions import *

class MongoQueryManager(QueryManager):

    """Class representing the mongo query manager used to interpret queries.

    The generic queries are converted into something pymongo (and by
    extension MongoDB) can understand and interpret.

    """

    def query(self, query):
        """Look for the specified objects."""
        model = query.first_model
        plural_name = get_plural_name(model)
        expression = self.get_expression(query)
        print("Expression", expression)
        return list(self.driver.datas[plural_name].find(expression))

    def get_expression(self, query):
        """Return the list containing the MongoDB expression."""
        and_expression = []
        or_expression = []
        for i, filter in enumerate(query.filters):
            if i > 0:
                connector = query.connectors[i]
                if connector == "or":
                    or_expression.append(
                            self.get_expression_from_filter(filter))
                    if and_expression:
                        or_expression.append(and_expression[-1])
                        del and_expression[-1]

                    continue

            and_expression.append(self.get_expression_from_filter(filter))

        expression = {}
        if and_expression:
            expression["$and"] = and_expression
        if or_expression:
            expression["$or"] = or_expression

        return expression

    def get_expression_from_filter(self, filter):
        """Return a simple expression (dictionary) from a filter."""
        operator = filter.operator.name
        converted_ops = {}
        if operator == "=":
            return {filter.field: filter.parameters[0]}
        else:
            converted_op = converted_ops[operator](filter)
            return {filter.field: converted_op, }

    def not_equal(self, filter):
        """Return the corresponding dictionary for the != operator."""
        return {"$ne": filter.parameters[0]}
