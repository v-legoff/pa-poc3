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


"""This module contains the List field type."""

import importlib

from model.types.base import BaseType
from model.represent import DCList

class List(BaseType):
    
    """Class representing a list field type.
    
    To create a list, you must specify (as a string) the field types that
    it should contain.  For instance, if a list must contain integers,
    write a model with this field definition:
        elements = List("Integer")
    
    Note that what you get when you further access the list is not a
    list type, but a representation.  You can manipulate it as a list,
    though, append or insert or delete elements from it even using
    slices.
    
    """
    
    type_name = "list"
    def __init__(self, contain_type, register=True):
        BaseType.__init__(self, pkey=False, default=None)
        self.register = register
        self.contain_type = None
        self.elements = DCList(self.model, self, [])
        if register and not contain_type:
            raise ValueError("a registered list MUST have a contain_type " \
                    "specified")
        
        if contain_type:
            # We try to find the type in types
            types = importlib.import_module("model.types")
            try:
                field_type = getattr(types, contain_type)
            except AttributeError:
                raise ValueError("the {} field type cannot be " \
                        "found".format(repr(contain_type))) from None
            
            if field_type not in [types.Integer, types.String]:
                raise ValueError("the {} field type can't be stored " \
                        "in a list".format(repr(contain_type)))
            
            self.contain_type = field_type
    
    def __get__(self, obj, typeobj):
        """Return the list representation."""
        if obj is None:
            return self
        
        return self.elements
    
    def __set__(self, obj, new_obj):
        """Try to set the related value.
        
        We DO NOT change the relation, but instead modify its content.
        
        """
        self.elements[:] = new_obj
