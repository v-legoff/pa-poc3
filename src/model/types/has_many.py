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


"""This module contains the HasMany relation field type."""

from model.represent import DCList
from model.types.base import BaseType
from model.types.list_pa import List

def get_pkey(mod_object):
    """Return the pkey value (not values)."""
    fields = [getattr(type(mod_object), name) for name in dir(type(
            mod_object))]
    fields = [field for field in fields if isinstance(field, BaseType)]
    field = [field.field_name for field in fields if field.pkey][0]
    return getattr(mod_object, field)

class HasMany(BaseType):
    
    """Class representing a has_many relation.
    
    Here is a snippet of code using relations:
        class User(Model):
            username = String()
            groups = HasMany("user.Group")
    
    When a relation HasMany is created, it creates in the model's table
    a transparent new attribute containing a list of referrence to
    the specified objects.  This relation is not visible (and should not be
    used directly) by the user.  The original attribute is a descriptor
    which will fetch the required objects, using the data connector.  Here's
    a snipset using the User model defined above:
    >>> me = User.find(id=1)  # it exists
    >>> print(me.group_ids)
    []
    >>> me.group_ids = [1]  # Add a group (one way)
    >>> me.group_ids
    [1]
    >>> me.groups
    [<user.Group model object>]
    >>> me.groups.append(Group.find(id=2)  # It exists too
    >>> me.group_ids
    [1, 2]
    >>> del me.groups[0]
    [2]
    
    """
    
    type_name = "has_many"
    def __init__(self, related_to, attribute_name=None):
        elts = []
        BaseType.__init__(self, pkey=False, default=elts)
        self.register = False
        self.related_to = related_to
        self._attribute_name = attribute_name
    
    @property
    def attribute_name(self):
        """Return the attribute name if set, otherwise a default one."""
        if self._attribute_name:
            return self._attribute_name
        
        attribute = self.field_name
        if attribute.endswith("ies"):
            attribute = attribute[:-3] + "y_ids"
        elif attribute.endswith("es"):
            attribute = attribute[:-2] + "_ids"
        elif attribute.endswith("s"):
            attribute = attribute[:-1] + "_ids"
        else:
            attribute += "_ids"
        
        return attribute
    
    def get_related(self, obj):
        """Return the link to the related_to field."""
        attribute_name = self.attribute_name
        return getattr(obj, attribute_name)
    
    def extend(self):
        """Extend the model."""
        attribute_name = self.attribute_name
        related = List("Integer")
        related.field_name = attribute_name
        related.model = self.model
        setattr(self.model, attribute_name, related)
    
    def __get__(self, obj, typeobj):
        """Try to access the related value."""
        if obj is None:
            return self
        
        keys = self.get_related(obj)
        data_connector = self.model.data_connector
        model = data_connector.models[self.related_to]
        objects = [model.find(key) for key in keys]
        elements = self.get_cache(obj)
        elements._elts[:] = objects
        
        return elements
    
    def __set__(self, obj, new_obj):
        """Try to set the related value.
        
        Simply update the lists.
        
        """
        elements = self.get_cache(obj)
        elements[:] = new_obj
    
    def get_cache(self, obj):
        """Return the cached list or create the DCList if needed."""
        field = self.field_name
        if field in obj._cache:
            return obj._cache[field]
        
        related = self.get_related(obj)
        elements = DCList(self.model, self, obj, [])
        elements.neighbor = related
        elements.to_neighbor = get_pkey
        obj._cache[field] = elements
        return elements
