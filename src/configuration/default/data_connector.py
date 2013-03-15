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


"""Module containing the DC (data connector) configuration."""

from configuration import *
from dc import connectors

def find_data_connector(dictionary):
    """Find the data connector according to the specified configuration.

    The name has already been provided.

    """
    name = dictionary["dc_name"]
    data_connector = connectors[name]
    configuration = data_connector.configuration
    configuration.validate(dictionary)
    
class DataConnectorConfiguration(Configuration):
    
    """Class defining the generic data connector's configuration.
    
    This configuration is a little complex, since each data connector has
    different configuration parameters.  Therefore, this
    must-remain-generic configuration just has a name and, based on this
    name, it should be able to find the expected data connector's
    configuration and apply it.
    
    The schema is defined after the 'find_data_connector' method.
    
    """
    
    schema = Schema("data_connector", definition={
            "dc_name": Data("the data connector's name", default="yaml"),
            "complements": find_data_connector,
    })
