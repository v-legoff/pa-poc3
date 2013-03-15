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


"""This module contains the DCList, detailed below."""

import collections

class DCList(collections.MutableSequence):
    
    """Class used to represent a list ocntaining DC objects.
    
    This class should have the behaviour of a list but each modification
    (append, insert, setitem with index or slice) should be reported to the
    model behind it.
    
    """
    
    def transform(self, i, value):
        """Transform the value for the neighbor, if any."""
        if self.to_neighbor:
            if isinstance(i, int):
                return self.to_neighbor(value)
            
            return [self.to_neighbor(v) for v in value]
        
        return value
    
    def __init__(self, model, field, object, elts):
        self._model = model
        self._field = field
        self._elts = elts
        self._object = object
        self.neighbor = None
        self.to_neighbor = None
    
    def __len__(self):
        return len(self._elts)
    
    def __getitem__(self, i):
        return self._elts[i]
    
    def __delitem__(self, i):
        del self._elts[i]
        self.del_structure(i)
    
    def __setitem__(self, i, values):
        self._elts[i] = values
        self.set_structure(i, values)
    
    def insert(self, i, value):
        self._elts.insert(i, value)
        self.add_structure(i, value)
    
    def __repr__(self):
        return repr(self._elts)
    
    def __str__(self):
        return str(self._elts)
    
    def add_structure(self, i, value):
        """Add the new object to the structure."""
        self.save()
        if self.neighbor is None:
            return
        
        value = self.transform(i, value)
        self.neighbor.insert(i, value)
    
    def set_structure(self, indice_or_slice, values):
        """Set the structure."""
        self.save()
        if self.neighbor is None:
            return
        
        values = self.transform(indice_or_slice, values)
        self.neighbor[indice_or_slice] = values
    
    def del_structure(self, indice_or_slice):
        """Del some of the structure."""
        self.save()
        if self.neighbor is None:
            return
        
        del self.neighbor[indice_or_slice]
    
    def save(self):
        """Save the list."""
        field = self._field
        field_name = field.field_name
        model = self._model
        object = self._object
        if field.register and model.data_connector and \
                model.data_connector.running:
            with model.data_connector.u_lock:
                model.data_connector.update_object(object, field_name, None)
