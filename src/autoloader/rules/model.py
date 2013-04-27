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


"""Module containing the ModelRule class."""

from autoloader.rules.base import Rule
from model.functions import get_name
from repository import Repository

class ModelRule(Rule):

    """Class defining the autoloader rule to import models.

    The models are module containing a class.  This class will be
    returned after importing the module.  Plus, this rule should:
    -   Try to find the corresponding repository and, if not found,
        create a default one
    -   Register the model in the proper bundle.

    """

    def __init__(self, server, data_connector):
        self.server = server
        self.data_connector = data_connector

    def load(self, module):
        """Load a specific module.

        This method:
            Get the Model class defined in the module
            Try to find the corresponding repository
            Write this dclass in the model's bundle
            Return the class

        """
        name = Rule.module_name(module)
        bundle_name = Rule.bundle_name(module)
        bundle = self.server.bundles[bundle_name]
        class_name = name.capitalize()
        mod_class = getattr(module, class_name)
        mod_class.bundle = bundle
        mod_name = get_name(mod_class)

        # Try to find the corresponding repository
        if mod_name in bundle.repositories:
            rep_class = bundle.repositories[mod_name]
            print("Found the repository", rep_class)
        else:
            rep_class = Repository
            print("Create a new repository")

        repository = rep_class(self.data_connector, mod_class)
        mod_class._repository = repository

        # Write the class in the bundles
        bundle.models[mod_name] = mod_class

        # Record the new bundle in the data connector
        self.data_connector.repository_manager.record_model(mod_class)

        return mod_class
