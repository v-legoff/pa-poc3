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


"""Module containing the Configuration class, defined below."""

import os

import yaml

from configuration.exceptions import *
from configuration.schema import Schema

class Configuration:

    """Class defining informations for a defined configuration.
    
    A configuration object is somewhat like a configuration file:  it
    contains some informations that can indicate some specific datas
    useful in a certain context.  But a Configuration object is more
    than a configuration file, since it stores a configuration schema
    describing what this configuration should contain.  It also specifies
    default values to use if the file doesn't indicate the desired data.
    
    Each configuration has:
        A schema (see the configuration.schema.Schema class)
        A default file, a path leading to a default configuration file
    
    """
    
    schema = None
    defaut_file = None
    
    @classmethod
    def validate(cls, configuration):
        """Validate a configuration.
        
        The configuration must be specified as a dictionary which
        will be confronted with the schema.
        If this method fails, an exception inherited from
        ConfigurationError will be raised.  Otherwise, the new object
        will be returned.
        
        """
        schema = cls.schema
        schema.validate(configuration)
        finale_configuration = cls()
        finale_configuration.datas.update(configuration)
        return finale_configuration
    
    @classmethod
    def read_YAML(cls, path, must_exist=False):
        """Read and try to build a configuration object.
        
        This class method tries to read the indicated file.  If the file
        exists, it is read with 'yaml'.  If the file doesn't exist,
        either an empty configuration object is created if the 'must_exist'
        parameter is set to False (the default), or a MissingFile
        exception is raised.
        
        """
        configuration = {}
        if not os.path.exists(path):
            if must_exist:
                raise MissingFile("the configuration file {} doesn't " \
                        "exist".format(repr(path)))
        elif not os.access(path, os.R_OK) and must_exist:
            raise MissingFile("the configuration file {} cannot be " \
                    "read".format(repr(path)))
        elif not os.path.isfile(path):
            raise MissingFile("the configuration file {} is not a file " \
                    "at all".format(repr(path)))
        else:
            with open(path, "r") as file:
                configuration = yaml.load(file)
        
        configuration = cls.validate(configuration)
        return configuration
    
    def __init__(self):
        """Constructor (DO NOT CALL DIRECTLY, use 'validate' instead)."""
        self.datas = {}
    
    def __repr__(self):
        return "<configuration (default={})>".format(self.default_file)
    
    def __str__(self):
        datas = self.datas.copy()
        to_display = []
        for name, value in datas.items():
            to_display.append(name + "=" + repr(value))
        
        return "Configuration with {}".format(", ".join(to_display))
    
    def __getitem__(self, data):
        return self.datas[data]
    
    def __setitem__(self, data, value):
        self.datas[data] = value
    
    def __contains__(self, data):
        return data in self.datas
    
    def __len__(self):
        return len(self.datas)
    
    def get(self, data, default=None):
        return self.datas.get(data, default)
