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


"""This package contains the Converter abstract class.

All converters should inherit from it.

"""

class Converter:
    
    """Abstract class to define a converter.
    
    This class is responsible for converting a specific field type (Integer, String, Date...) in two ways:
        Storage to object
        Object to storage
    
    The first one uses the 'to_object' method.  It is called when an object
    is loaded with the data connector.  Therefore, this method should return
    the write object (the returned value will be set as the object attribute).
    
    The second one uses the 'to_storage' method and is called when an object
    must be stored in a data connector.  It should return the value to store
    (maybe you want a DateTime type field to be stored as a string).
    
    The two methods should be compatible:  if an object field is stored as a
    certain value, it should be possible to this converter to convert
    the value back to an object field.
    
    """
    
    @staticmethod
    def to_object(value):
        """Return the value which will be used as the object attribute.
        
        This method expects the value stored by the data connector and should
        return the value that the Python object should contain as an instance
        attribute.  The default behaviour is to return the stored
        value without modification.
        
        """
        return value
    
    @staticmethod
    def to_storage(value):
        """Return the value to be stored in the data connector.
        
        This method expects the value used by Python as an instance
        attribute of a model object.  It should return the value that
        will be stored in the data connector.  By default, the same
        value is returned without modification.
        
        """
        return value
