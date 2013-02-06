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
    
    def __init__(self, model, field, elts):
        self._model = model
        self._field = field
        self._elts = elts
    
    def __len__(self):
        return len(self._elts)
    
    def __getitem__(self, i):
        return self._elts[i]
    
    def __delitem__(self, i):
        self.del_structure(i)
        del self._elts[i]
    
    def __setitem__(self, i, values):
        self.set_structure(i, values)
        self._elts[i] = values
    
    def insert(self, i, value):
        self.add_structure(i, value)
        self._elts.insert(i, value)
    
    def __repr__(self):
        return repr(self._elts)
    
    def __str__(self):
        return str(self._elts)
    
    def add_structure(self, i, value):
        """Add the new object to the structure."""
        print("Add structure", i, value)
    
    def set_structure(self, indice_or_slice, values):
        """Set the structure."""
        print("Set structure", indice_or_slice, values)
    
    def del_structure(self, indice_or_slice):
        """Del some of the structure."""
        print("Del structure", indice_or_slice)
