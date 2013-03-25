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


"""Module containng the abstract Command class."""

from argparse import ArgumentParser
import os
import shlex
import sys
import textwrap

from command.meta import MetaCommand

class Command(metaclass=MetaCommand):

    """Abstract class representing a command.

    Each command should inherit from this class.

    """

    brief = "an unknown command to do something"
    description = "do something, I don't know what"
    name = None
    parent = None
    def __init__(self):
        """Create a new command.

        You should indicate its name.

        Note: it does create a new command but does not add it in a tree.  The
        'parent' class attribute is therefore not used yet.  A command without
        a tree can be processed, that is executed with some arguments
        (see the 'process' method).

        """
        self.tree = None
        self.parser = ArgumentParser(
                description=self.description,
        )
        self.children = []
        self.project_created = True #  should the project already exist?

        # Add default command
        self.parser.add_argument(
                "--path",
                help="the path leading to the user's configuration",
                default=os.getcwd(),
            )

    @property
    def fullname(self):
        """Return the command's full name if the tree is set.

        The command's full name is the name of all its successive parents.
        If no tree is set, the name of the command itself is returned.

        """
        if self.tree is None or self.parent is None:
            return self.name
        elif isinstance(self.parent, str):
            return self.parent + " " + self.name
        else:
            return self.parent.fullname + " " + self.name

    def process(self, to_interpret):
        """Process the command.

        This method expects a string or list of arguments as a parameter.  If
        a string is specified, then the module shlex (and its function
        'split') is used.  Otherwise, the list is used directly.  You can
        call this method without a tree by calling 'process' with
        sys.argv[1:] as an argument to use the parameters given to the
        command-line, for instance.

        """
        if isinstance(to_interpret, str):
            to_interpret = shlex.split(to_interpret)
        elif not isinstance(to_interpret, list):
            raise TypeError("this function expects a list or string")

        # Now 'to_interpret' should be a list of strings
        result = self.parser.parse_args(to_interpret)
        return self, result

    def execute(self, namespace):
        """Method called when the command options were correctly parsed.

        This method is automaticcaly called by the 'process' method if no
        error occured during the command parsing.  If everything goes right,
        then the 'execute' method is called with the resulting namespace
        which contains the specified arguments parsed by argparse.  The
        ONLY case when you create a command without redefining its
        'execute' method is when you only need a command that acts as
        a container (that is, a command that can't be executed on
        itself, but displays the available choices to the user).

        """
        self.display_help()

    def display_help(self, file=sys.stdout):
        """Display the command help message.

        You can specify a different file to print the message somewhere else than to the default output.

        """
        message = "Command: " + self.fullname + "\n\n"
        description_lines = textwrap.wrap(self.description, width=75)
        wrapped_description = "\n    ".join(description_lines)
        message += "    " + wrapped_description
        if self.children:
            message += "\n\nAvailable sub-commands:"
            for command in self.children:
                message += "\n    " + command.name
                message += " - " + command.brief

        print(message, file=file)
