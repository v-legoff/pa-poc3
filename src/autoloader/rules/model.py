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

class ModelRule(Rule):
    
    """Class defining the autoloader rule to import models.
    
    The models are module containing a class.  This class will be
    returned after importing the module, but the data_connector
    class attribute of this newly imported class should be set,
    as well.
    Plus, the model should register itself in the proper bundle.
    
    """
    
    def __init__(self, server, data_connector):
        self.server = server
        self.data_connector = data_connector
    
    def load(self, module):
        """Load a specific module.
        
        This method:
            Get the Model class defined in the module
            Set the data_connector class attribute of this class
            Write this dclass in the model's bundle
            Return the class
        
        """
        name = Rule.module_name(module)
        class_name = name.capitalize()
        mod_class = getattr(module, class_name)
        mod_class.data_connector = self.data_connector
        self.data_connector.record_model(mod_class)
        
        # Write the class in the bundles
        bundle_name = Rule.bundle_name(module)
        self.server.bundles[bundle_name].models[class_name] = mod_class
        return mod_class
