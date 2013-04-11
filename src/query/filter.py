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


"""Module containing the Filter class, described below."""

import re

from query.operators import OPERATORS

# We select the operators used with the syntax "field, operator, value"
OPS_FOV = [re.escape(name) for name, op in OPERATORS.items() if \
        op.field_first]

# We select the operators used with the syntax "value, operator, field"
OPS_VOF = [re.escape(name) for name, op in OPERATORS.items() if \
        not op.field_first]

# Then we define the regex
REGEX_FOV = re.compile(r"^([A-Za-z0-9]+)\s*({})\s*\?$".format(
        "|".join(OPS_FOV)))
REGEX_VOF = re.compile(r"^\?\s*({})\s*([A-Za-z0-9]+)$".format(
        "|".join(OPS_VOF)))

class Filter:

    """Class representing a very simple filter.

    This class should define a simple filter composed with three arguments:
        The field's name
        The operator
        The tested value

    They can be in the other way if the operator expects it (a "in"
    operator, for instance, requires first the value and after the
    field's name).

    These filters can be chained to obtain a more complicated
    filter.

    """

    def __init__(self, expression, parameter):
        regex = REGEX_FOV.search(expression)
        if regex is None:
            regex = REGEX_VOF.search(expression)
            if regex is None:
                raise ValueError("incorrect syntax: {}".format(
                        repr(expression)))

            op_name, field = regex.groups()
        else:
            field, op_name = regex.groups()

        # Select the operator
        operator = OPERATORS.get(op_name)
        if operator is None:
            raise ValueError("unknown operator: {}".format(repr(op_name)))

        self.field = field
        self.operator = operator
        self.parameter = parameter

    def __str__(self):
        if self.operator.field_first:
            rep = "{field} {operator} {parameter}"
        else:
            rep = "{parameter} {operator} {field}"

        return rep.format(field=self.field, operator=self.operator.name,
                parameter=self.parameter)
