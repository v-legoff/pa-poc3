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


"""Module containing the class Data detailed below."""

from configuration.exceptions import *

class Data:

    """Class defining a configuration data.
    
    Such datas are used to represent an expected configuration information,
    like a valid IP address.  It can define default values and convertion
    callables.
    
    """
    
    def __init__(self, description, default=None, type=str, required=False):
        """Create a new data.
        
        Expected arguments:
            description -- a string describing the data (for displaying errors)
            default -- the default value
            type -- the data's type (callable [1])
            required -- is this data mandatory?
        
        [1] The type can be a tuple or a simple callable.  If it's a
            callable, it should be used to convert the original data and,
            if impossible, raise a ValueError.  You can use the 'int',
            'float' or 'str' builtin functions.  You can also provide a tuple
            of classes if you can exploit several different types.  The
            'isinstance' function is used to test them.  To learn more,
            read the 'convert' method.
        
        """
        self.name = "not set"
        self.description = description
        self.default = default
        self.type = type
        self.required = required
    
    def convert(self, value):
        """Try to convert the data using the type.
        
        A convertion may not be necessary.  This method first tests
        the provided value with the 'isinstance' builtin function.  If
        this function returns False, then this method attempts to convert
        the value with the provided classes or callables.  The first
        convertion that succeeds (don't raise any exception) is
        returned.  If everything still fails, raise a BadDataType
        exception.
        
        Only use this method if necessary:  if the data is not provided,
        you should either raise a MissingData exceptio if the data
        is required or simply return the default value.
        
        """
        good_type = isinstance(value, self.type)
        if good_type:
            return value
        
        types = self.type
        if callable(types):
            types = [types]
        
        for function in types:
            try:
                converted = function(value)
            except ValueError:
                continue
            else:
                return converted
        
        # Convertion impossible
        raise BadDataType("the data {} ({}) is not of the right type;  " \
                "expected {}, got {} ({})".format(self.name, self.description,
                self.type, repr(value), type(value)))
    
    def validate(self, value):
        """Validate the data.
        
        If this method succeeds, return the data (it may be different if
        converted).  If it fails, raise an exception inherited
        from ValidationError.
        
        """
        if value is None: #  we assume it hadn't been provided
            if self.required:
                raise MissingData("the mandatory data {} ({}) wasn't " \
                        "provided".format(self.name, self.description))
            
            return self.default
        
        return self.convert(value)
