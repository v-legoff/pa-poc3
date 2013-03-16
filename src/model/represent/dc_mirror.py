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


"""This module contains the DCMirror class, detailed below."""

import collections

class DCMirror(collections.MutableSequence):
    
    """Class used to represent a mirror on a list.
    
    A mirrored list is connected to a DCList.  It watches the neighbor
    list and each modification attempt is transferred to the neighbor
    list.  It is not exactly the neighbor list (otherwise, it won't be
    very useful in the first place) and has two methods, 'to_neighbor'
    and 'to_mirror' that are used to convert the list elements.
    
    """
    
    @staticmethod
    def to_neighbor(element):
        """Transform a single element before updating the neighbor."""
        pass
    
    @staticmethod
    def to_mirror(element):
        """Convert an element from the neighbor to the mirrored list"""
        pass
    
    def convert_to_neighbor(self, i, value):
        """Transform the value for the neighbor."""
        if isinstance(i, int):
            return self.to_neighbor(value)
        
        return [self.to_neighbor(v) for v in value]
    
    def convert_to_mirror(self, i, value):
        """Transform the value for the mirror."""
        if isinstance(i, int):
            return self.to_mirror(value)
        
        return [self.to_mirror(v) for v in value]
    
    def __init__(self, neighbor):
        self.neighbor = neighbor
    
    def __len__(self):
        return len(self.neighbor)
    
    def __getitem__(self, i):
        elements = self.neighbor[i]
        elements = self.convert_to_mirror(i, elements)
        return elements
    
    def __delitem__(self, i):
        del self.neighbor[i]
    
    def __setitem__(self, i, values):
        values = self.convert_to_neighbor(i, values)
        self.neighbor[i] = values
    
    def insert(self, i, value):
        value = self.convert_to_neighbor(i, value)
        self.neighbor.insert(i, value)
    
    def __repr__(self):
        values = self.convert_to_mirror(slice(None), self.neighbor)
        return repr(values)
    
    def __str__(self):
        values = self.convert_to_mirror(slice(None), self.neighbor)
        return str(values)
