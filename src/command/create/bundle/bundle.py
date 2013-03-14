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


"""Module containing the create bundle default command."""

import os

from command import *

class Bundle(Command):
    
    """Command 'create bundle'.
    
    This command is used to create a new bundle, that is the bundle directory
    and its content on a stantd basis.  If the '--default' option is
    specified, then the bundle is create based on default
    configuration.  However, if no 'default' option is supplied, then
    the bundle is created in 'interactive mode', so several questions
    are directly asked to the user before creating the bundle.
    For instance, the user can create controllers, routes, models and
    services.  Of course, she will need to edit the files afterward
    because they will be somewhat empty.
    
    """
    
    name = "bundle"
    parent = "create"
    brief = "create a new bundle"
    description = \
        "This command is used to create a new bundle.  You must execute it " \
        "in the user's directory where you want to add the new bundle " \
        "(the new bundle's name will be a directory created in the " \
        "'bundles/{name}' directory).  Note that the '--default' option " \
        "allows you to create a bundle without prompting for additional " \
        "informations.  It is, therefore, useful if you wish to create a " \
        "new bundle automatically."
    
    def __init__(self):
        Command.__init__(self)
        self.parser.add_argument("name", help="the new bundle's name")
        self.parser.add_argument("--default", action="store_true")
    
    def execute(self, namespace):
        """Execute the command."""
        # First, check that the bundle as a valid name
        name = namespace.name.lower()
        path = namespace.path
        directory = path + os.sep + "bundles" + os.sep + name
        if os.path.exists(directory):
            raise InteruptCommand("the directory {} already exists".format(
                    repr(directory)))
        
        os.makedirs(directory)
        print("Bundle {} created".format(repr(name)))
