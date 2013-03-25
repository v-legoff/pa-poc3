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


"""Module containing the Tree class, defined below."""

import shlex

from command.meta import COMMANDS

class Tree:

    """A tree of commands.

    A tree can create and walk through a hierarchy of commands.  Commands may
    be defined by default (in the package commands) or in the user's
    configuration.  In any case, the tree is composed of a list of
    commands, first-level ones (that is, the ones without a defined parent).
    Each command may have other sub-commands.

    """

    def __init__(self):
        """Build an empty command tree;"""
        self.commands = []
        self.fullnames = {}

    def __repr__(self):
        commands = ", ".join([command.name for command in self.commands])
        return "<CommandTree with {}>".format(commands)

    def add_default_commands(self):
        """Add the default commands, defined in the command.COMMANDS constant.

        This method should be called automatically and CANNOT be used
        to add new commands defined in the user's configuration.

        """
        self.add_commands(COMMANDS)

        for command in self.fullnames.values():
            # Now bind each command's parent
            if command.parent:
                parent = self.fullnames.get(command.parent)
                if parent is None:
                    raise ValueError("the {} command defines an unknown {} " \
                            "parent".format(repr(command.fullname),
                            repr(command.parent)))

                command.parent = parent
                parent.children.append(command)

    def add_commands(self, commands):
        """Recursively add a list of commands."""
        for command_class in commands:
            if command_class.name:
                command = command_class()
                self.add_command(command)

    def add_command(self, command):
        """Add the new command to the tree."""
        if command.parent is None:
            self.commands.append(command)

        self.fullnames[command.fullname] = command

    def process(self, to_interpret):
        """Walk the tree to find the right command.

        Like the Command.process function, it accepts a list of strings or a string.  In the former case, it is used directly.  In the later one, it is converted in a list using 'shlex.split'.

        """
        if isinstance(to_interpret, str):
            to_interpret = shlex.split(to_interpret)
        elif not isinstance(to_interpret, list):
            raise TypeError("this function expects a list or string")

        # Recursively walk through the tree
        return self.find_command(to_interpret)

    def find_command(self, to_interpret, commands=None, parent=None):
        """Recursively find a command.

        If it's not found, display the help of the last parent found, if any.

        """
        if commands is None:
            commands = self.commands

        name = to_interpret and to_interpret[0].lower() or ""
        for command in commands:
            if command.name == name:
                if command.children:
                    return self.find_command(to_interpret[1:],
                            command.children, command)
                else:
                    return command.process(to_interpret[1:])

        if parent:
            parent.display_help()
        else:
            message = "Python Aboard Command Line\n\n"
            message += "Use one of the following sub-command:"
            for command in self.commands:
                message += "\n    " + command.name
                message += " - " + command.brief

            print(message)

        return None, None
