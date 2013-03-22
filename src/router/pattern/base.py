# Copyright (c) 2012 LE GOFF Vincent
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


"""This module contains the different pattern types."""

from router.pattern.meta import *

class PatternType(metaclass=PatternMeta):

    """Abstract class which represents a pattern type.

    The 'pattern' used in this context is a part of a route.  This pattern
    isused to represent dynamic part in a route.  For instance, in the route
    'images/{id}', the 'id' part is dynamic.  when the route is built,
    the corresponding pattern (id) is called.  Each pattern type is a
    subclass of 'PatternType'.

    To add a new default pattern type:
    *  Create a new module in this package using the pattern's name
    *  Insert in it a subclass of PatternType, detailled below
    *  Import this pattern type in the pattern package.

    If you want to create a bundle that add new pattern types, the process
    is of course different.

    A pattern type needs some informations:

    Class attributes (or property):
        regex -- the regular expression as a str [1]

    Instance methods:
        convert -- convert the dynamic part (still str)

    """

    name = None #  Specify it in a subclass
    regex = None #  Specify it in the subclass (or a property object)

    def __init__(self, route, required=True):
        """Create a new pattern."""
        self.route = route
        self.required = required

    @property
    def full_regex(self):
        """Reurn the full regex, with group and required included.

        You SHOULD NOT redifine this property in a subclass (instead set
        regex).

        """
        regex = "(" + self.regex + ")"
        if not self.required:
            regex += "?"

        return regex

    def convert(self, expression):
        """Return the converted expression if possible.

        If not, raise a PatternError exception.

        """
        raise NotImplementedError

    @staticmethod
    def find_and_create(route, pattern_definition):
        """Try to find the pattern type."""
        required = True
        if pattern_definition.startswith("?"):
            pattern_definition = pattern_definition[1:]
            required = False

        pattern_type = TYPES[pattern_definition]
        return pattern_type(route, required=required)
