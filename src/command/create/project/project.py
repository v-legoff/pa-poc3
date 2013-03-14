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


"""Module containing the create project default command."""

import os

from command import *

class Project(Command):
    
    """Command 'create project'.
    
    This command is used to create a project, that is one new "user
    directory" with an empty structure.
    
    """
    
    name = "project"
    parent = "create"
    brief = "create a new project"
    description = \
        "This command is used to create a new project.  You can use " \
        "the '--path' option to specify the parent directory (that must " \
        "exist).  Otherwise, the current directory will be used.  You " \
        "have to specify the project's name.  A new directory of the " \
        "specified name will be created in the selected path.  A default " \
        "structure will be created (an empty bundle container, a default " \
        "layout, a default configuration).  Some informations could " \
        "be directly prompted by the tool, unless you specify the " \
        "'--default' option."
    
    def __init__(self):
        Command.__init__(self)
        self.project_created = False
        self.parser.add_argument("name", help="the new project's name")
        self.parser.add_argument("--default", action="store_true")
    
    def execute(self, namespace):
        """Execute the command."""
        name = namespace.name.lower()
        path = namespace.path
        if not os.path.exists(path):
            raise ValueError("the directory {} does not exist".format(
                    repr(path)))
        
        if not os.access(path, os.W_OK):
            raise ValueError("the path {} is not writable".format(
                    repr(path)))
        
        directory = path + os.sep + name
        if os.path.exists(directory):
            raise InteruptCommand("the directory {} already exists".format(
                    repr(directory)))
        
        os.makedirs(directory)
        default_dirs = (
            "bundles",
            "config",
            "layout",
            "plugins",
            "static",
        )
        
        for dirname in default_dirs:
            os.makedirs(directory + os.sep + dirname)
        
        # Create the default configuration
        print("done")
