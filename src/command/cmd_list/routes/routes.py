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


"""Module containing the 'list routes' default command."""

from command import Command
from display.table import Table

class Routes(Command):

    """Command 'list routes'.

    This command is used to list the defined routes.

    """

    name = "routes"
    parent = "list"
    brief = "list the defined routes"
    description = \
        "This command lists the defined routes."

    def __init__(self):
        Command.__init__(self)
        self.parser.add_argument("-m", "--methods", action="store_true",
                help="display the HTTP methods for each route")
        self.parser.add_argument("-P", "--sort-by-pattern",
                action="store_true", help="sort the lines by pattern")

    def execute(self, namespace):
        """Execute the command."""
        routes = sorted(self.server.dispatcher.routes.copy().values(),
                key=lambda route: (route.bundle_name, route.controller_name,
                route.action_name))

        # Constitute the table
        table = Table("Pattern", "Bundle", "Controller", "Action",
                left_border="  ", right_border="")

        if namespace.methods:
            table.add_column("Methods")

        for route in routes:
            row = table.add_row(route.pattern, route.bundle_name,
                    route.controller_name, route.action_name)

            if namespace.methods:
                row.set("Methods", route.pretty_methods)

        if namespace.sort_by_pattern:
            if namespace.methods:
                table.sort_by("Pattern", "Methods")
            else:
                table.sort_by("Pattern")

        print(table)
