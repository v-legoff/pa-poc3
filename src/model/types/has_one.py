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


"""This module contains the HasOne relation field type."""

from model.types.base import BaseType
from model.types.integer import Integer

class HasOne(BaseType):
    
    """Class representing a has_one relation.
    
    Here is a snippet of code using relations:
        class User(Model):
            username = String()
            group = HasOne("user.Group")
    
    When a relation HasOne is created, it creates in the model's table
    a transparent new attribute containing a single referrence to an
    object (or None).  This relation is not visible (and should not be
    used directly) by the user.  The original attribute is a descriptor
    which will fetch the required object, using the data connector.  Here's
    a snipset using the User model defined above:
    >>> me = User.find(id=1)  # it exists
    >>> print(me.group_id)
    None
    >>> me.group_id = 1 # change the group
    >>> me.group_id
    1
    >>> me.group
    <user.Group model object>
    >>> me.group.name
    "the first group"
    >>> me.group = Group.find(id=2)
    >>> me.group.name
    "the second group"
    >>> me.group_id
    2
    
    """
    
    type_name = "has_one"
    def __init__(self, related_to, attribute_name=None):
        BaseType.__init__(self, pkey=False, default=None)
        self.register = False
        self.related_to = related_to
        self._attribute_name = attribute_name
    
    @property
    def attribute_name(self):
        """Return the attribute name if set, otherwise a default one."""
        if self._attribute_name:
            return self._attribute_name
        
        attribute_name = self.field_name + "_id"
        return attribute_name
    
    def get_related(self, obj):
        """Return the link to the related_to field."""
        attribute_name = self.attribute_name
        return getattr(obj, attribute_name)
    
    def extend(self):
        """Extend the model."""
        attribute_name = self.attribute_name
        related = Integer(default=lambda o: None)
        related.field_name = attribute_name
        related.model = self.model
        related.set_default = False
        setattr(self.model, attribute_name, related)
    
    def __get__(self, obj, typeobj):
        """Try to access the related value."""
        if obj is None:
            return self
        
        key = self.get_related(obj)
        data_connector = self.model.data_connector
        model = data_connector.models[self.related_to]
        if key is None:
            return None
        
        return model.find(key)
    
    def __set__(self, obj, new_obj):
        """Try to set the related value.
        
        We change the attribute_name value on the object depending on the
        given the new_obj's primary keys.
        
        """
        attribute_name = self.attribute_name
        data_connector = self.model.data_connector
        model = data_connector.models[self.related_to]
        if new_obj is None:
            new_value = None
        else:
            if not isinstance(new_obj, model):
                raise ValueError("try to affect {} to the {}.{} model " \
                        "field".format(new_obj, self.model, self.field_name))
            
            fields = [getattr(model, name) for name in dir(model)]
            fields = [field for field in fields if isinstance(field, BaseType)]
            fields = sorted(fields, key=lambda field: field.nid)
            p_fields = [field.field_name for field in fields if field.pkey]
            values = []
            for attr in p_fields:
                values.append(getattr(new_obj, attr))
            
            if len(values) == 1:
                values = values[0]
            
            new_value = values
        
        setattr(obj, attribute_name, new_value)
