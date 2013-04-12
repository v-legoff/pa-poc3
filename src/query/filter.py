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

from query.operators import OPERATORS

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

    def __init__(self, expression, *parameters):
        for regular_expression, cls_operator in OPERATORS.items():
            match = regular_expression.search(expression)
            if match:
                field = match.groups()[0]
                operator = cls_operator(field, *parameters)
                self.field = field
                self.operator = operator
                self.parameters = parameters
                break

        if not match:
            raise ValueError("incorrect syntax: {}".format(
                    repr(expression)))

    def __repr__(self):
        return "<query.filter.Filter with {}>".format(str(self.operator))

    def __str__(self):
        return str(self.operator)
