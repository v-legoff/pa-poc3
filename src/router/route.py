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


"""This module contains the route class, a route definition."""

import re

from router.pattern.base import PatternType

# Constants
RE_PATTERNS = re.compile(r"\{(.*?)\}")

class Route:

    """A route definition for the Python Aboard dispatcher.

    This class describes the concept of routes, which are used to
    match an URI to a corresponding callable.  When the AboardDispatcher
    receives a URI, it browses the defined routes to find one that matches
    it.  The first found one will be used and its callable will be
    called with some specific arguments.

    When a route is defined by the user, she provides the static part
    as usal with the dynamic part between braces.  For instance:
        /users/{id}
    Here, '/users' is the URI's static part.  It won't change.  But the
    '{id}' part is a pattern.  It will be converted to a special regular
    expression.  So this route definition will be converted to:
        '\\/users\\/(\d+)'

    How a pattern ('id' in this example) is converted to a regular
    expression is described in the 'pattern.py' file.

    """

    format_dependent = False
    def __init__(self, pattern, controller, callable, methods=None):
        """Create a new route.

        Expected parameters:
            pattern -- the pattern representing the match
            controller -- the controller (Controller object)
            callable -- the callable called if the route matches
            methods -- a list of valid method for this route (list of strings)

        """
        if pattern.endswith("/"):
            pattern = pattern[:-1]

        self.pattern = pattern
        self.controller = controller
        self.callable = callable
        if isinstance(methods, str):
            methods = [methods]
        if methods:
            methods = tuple(name.upper() for name in methods)

        self.methods = methods
        self.bundle = None
        self.controller_name = ""
        self.action_name = ""
        self.py_pattern = ""
        self.re_pattern = ""
        self.patterns = []

        # Convert the pattern to a regular expression
        self.convert_pattern(pattern)

    def __repr__(self):
        methods = self.pretty_methods
        return "<Route to {} -> {} (methods={})>".format(
                self.pattern, self.controller, methods)

    def __call__(self, *matches, **kwargs):
        """Call the route's callable.

        This method converts the dynamic part of the URI.

        """
        matches = list(matches)
        for i, match in enumerate(matches):
            if match is not None:
                pattern = self.patterns[i]
                matches[i] = pattern.convert(match)

        return self.callable(*matches, **kwargs)

    @property
    def bundle_name(self):
        """Return the bundle's name."""
        return self.bundle and self.bundle.name or ""

    @property
    def pretty_methods(self):
        """Return a string representing the methods."""
        methods = self.methods
        if methods is None:
            methods = "all"
        else:
            methods = ", ".join(methods)

        return methods

    def match(self, request, path):
        """Return whether or not thie path is matched by the route."""
        if self.methods and request.method.upper() not in self.methods:
            return False

        match = self.re_pattern.search(path)
        if match:
            return match.groups()

        return False

    def get_path(self, *arguments):
        """Return the route with its arguments."""
        return self.py_pattern.format(*arguments)

    def convert_pattern(self, pattern):
        """Return the regular expression corresponding to the specified pattern.

        If errors are found, this method will raise specific
        exceptions inherited from PatternError.

        """
        re_pattern = ""
        py_pattern = ""
        pattern_types = []
        pos = 0
        while pos is not None:
            # Get the string from pos to the end
            sub = pattern[pos:]
            pattern_match = RE_PATTERNS.search(sub)
            if pattern_match:
                start = pattern_match.start()
                pos = pattern_match.end()
                pattern_def = pattern_match.groups()[0]
                pattern_type = PatternType.find_and_create(self, pattern_def)
                before = sub[:start]
                py_pattern += before + "{}"
                re_pattern += re.escape(before)
                re_pattern += pattern_type.full_regex
                pattern_types.append(pattern_type)
            else:
                pos = None
                py_pattern += sub
                re_pattern += sub

        re_pattern = "^" + re_pattern + "$"
        self.py_pattern = py_pattern
        self.re_pattern = re.compile(re_pattern)
        self.patterns = pattern_types
