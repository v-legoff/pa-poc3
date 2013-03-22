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


"""Module defining the Controller class, described below."""

import cherrypy

from formatters import formats
from model.exceptions import ObjectNotFound

class Controller:

    """Class describing a controller, wrapper for actions.

    A controller is a class containing methods that will act as actions.  If a
    route is connected to an action of a controller (a method of the class),
    then it will be called when a request is sent to this route.

    """

    server = None
    def __init__(self, bundle):
        """Build the controller."""
        self.bundle = bundle

    @property
    def request(self):
        """Return the serving Cherrypy request."""
        return cherrypy.serving.request

    @property
    def requested_format(self):
        """Return the requested format."""
        path = self.request.path_info
        format = path.split(".")[-1]
        if len(format) == len(path):
            # The format is not defined
            format = ""

        return format

    @staticmethod
    def authenticated(function):
        """Prevent any no-logged-in users to access the action."""
        def callable_wrapper(controller, *args, **kwargs):
            """Wrapper of the controller."""
            if controller.server.authenticated():
                return function(controller, *args, **kwargs)

            return "You are not logged in."
        return callable_wrapper

    def render(self, view, **representations):
        """Render datas using the formatters."""
        format = self.requested_format
        if not format:
            format = self.server.default_format

        if format not in self.server.allowed_formats:
            return "Unknown format {}.".format(format)

        return formats[format].render(view, **representations)

    def get_cookie(self, name, value=None):
        """Return, if found, the cookie.

        Otherwise, return value.


        """
        return self.server.get_cookie(name, value)

    def set_cookie(self, name, value, max_age, path="/", version=1):
        """Set a cookie."""
        self.server.set_cookie(name, value, max_age, path, version)
