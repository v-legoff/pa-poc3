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


import re

"""Module containing the base class Operator, defined below."""

# Constants
FIELD = r"[A-Za-z_][A-Za-z0-9_]*"

class Operator:

    """Operator base class, used to represent a generic query operator.

    The operator defined by this class should remain generic so
    every data connector could interpret a filter with this operator.
    The mechanism to "convert" a generic operator to an understandable
    operator used by a selected data connector is contained in the
    data connector itself.

    """

    name = None
    expression = ""
    nb_parameters = 1

    @classmethod
    def compile_regular_expression(cls):
        """Compare the regular expression based on the expression.

        The expression should be a string containing format-strings like:
            {field} -- the field's name
            {operator} -- the operator's name
            {parameter} -- a parameter

        Here's a simple example:
            expression = "{field}{operator}{parameter}"

        """
        field = "(" + FIELD + ")"
        operator = r"\s*" + re.escape(cls.name) + r"\s*"
        parameter = r"\?"
        parameters = cls.nb_parameters * [parameter]
        expression = cls.expression.format(*parameters, operator=operator,
                field=field)
        return re.compile(expression)

    def __init__(self, field, *parameters):
        self.field = field
        self.parameters = parameters

    def __str__(self):
        parameters = [repr(parameter) for parameter in self.parameters]
        return type(self).expression.format(*parameters, field=self.field,
                operator=type(self).name)
