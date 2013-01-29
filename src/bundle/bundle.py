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


"""Module containing the Bundle class, defined below."""

import os

import yaml

from bundle.config import Config
from bundle.meta_datas import MetaDatas

class Bundle:
    
    """Class representing a user bundle, part of a Python Aboard application.
    
    The bundles defined by the user contains part of his application.  The
    whole bundles almost constitute the entire application itself.
    As a matter of fact, the bundle contains:
    *   Configuration (like, for instance, routing informations)
    *   Controllers and their actions
    *   Models
    *   Views (templates)
    
    The bundles should be as independant as possible:  removing a bundle may
    remove some functionalities but the application should still
    work.  Though, some bundles may need other bundles to work and,
    if so, they won't be installed at all if some requirements are
    missing.
    
    """
    
    def __init__(self, server, name):
        """Create a new bundle."""
        self.server = server
        self.name = name
        self.meta_data = None
        self.controllers = {}
        self.models = {}
        self.views = {}
        self.config = None
    
    def setup(self, server, loader):
        """Setup the bundle following the setup process.
        
        Note that the bundles dictionary is passed to the setup method.  It
        allows the bundle, when reading its meta-datas, to check its
        requirements.
        
        Return whether the bundle has been correctly setup.  If the
        setup method returns False, the bundle won't be used in the
        final application.
        
        When the server is running, all installed bundles are read and setup
        following this process:
        1.  The bundle meta-datas are read from its file bundle.py.  If this
            meta-datas indicates that the bundle can not be setup, the process
            stops
        2.  The controllers, models and views are loaded
        3.  The configuration is read and follows its own setup process
        
        """
        fs_root = self.server.user_directory
        self.meta_datas = self.read_meta_datas()
        
        # Check the bundle requirements
        for requirement in self.meta_datas.requirements:
            if requirement not in server.bundles:
                print("The {} bundle needs the {} one".format(
                        self.name, requirement))
                return False
        
        for plugin_name in self.meta_datas.plugins:
            self.server.plugin_manager.load_plugin(loader, plugin_name)
            self.server.plugin_manager.call("extend_autoloader",
                    self.server, loader)
            self.server.plugin_manager.call_for(plugin_name,
                    "bundle_autoload", self, loader)
        
        # Load the bundle's configuration
        self.config = Config(self.server, self.name)
        cfg_setup = self.config.setup(server)
        if not cfg_setup:
            return False
        
        # Load (with the autoloader) the Python modules
        loader.load_modules("controller", \
                "bundles." + self.name + ".controllers", fs_root)
        loader.load_modules("model", "bundles." + self.name + ".models",
                fs_root)
        loader.load_modules("service", "bundles." + self.name + ".services",
                fs_root)
        return True
    
    def read_meta_datas(self):
        """Read the meta datas."""
        path = os.path.join(self.server.user_directory, "bundles", self.name,
                "bundle.yml")
        if not os.path.exists(path):
            raise ValueError("the meta-datas of the {} bundle can't " \
                    "be found in {}".format(self.name, path))
        
        if not os.access(path, os.R_OK):
            raise ValueError("the meta-datas of the {} bundle can't " \
                    "be read in {}".format(self.name, path))
        
        with open(path, "r") as meta_file:
            meta_dict = yaml.load(meta_file)
        
        return MetaDatas(self.name, meta_dict)
