# Copyright (c) 2012 LE GOFF Vincent
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


"""This module contains the data types supported by Python Aboard.

Each field is defined in a class inheited from BaseType (see below).

"""

import copy

class BaseType:
    
    """Class representing an abstract type of field.
    
    Each created field has a 'nid' attribute, which represent its identifier
    different from all other types, no matter the field type or the model
    in which it is defined.  This identifier is used to order the fields
    for an object.
    
    """
    
    current_nid = 1
    
    @classmethod
    def next_nid(cls):
        nid = BaseType.current_nid
        BaseType.current_nid += 1
        return nid
    
    type_name = "undefined"
    def __init__(self, pkey=False, default=None):
        """The basetype field constructor."""
        self.nid = self.next_nid()
        self.model = None
        self.field_name = "unknown name"
        self.pkey = pkey
        self.auto_increment = False
        self.default = default
        self.register = True
        
        if default:
            if not callable(default):
                # Check that the default value is accepted
                self.accept_value(default)
    
    def __repr__(self):
        return "<field {} ({})>".format(repr(self.field_name), self.nid)
    
    def copy(self):
        """Return a shallow copy of self."""
        copied = copy.copy(self)
        copied.nid = self.next_nid()
        return copied
    
    def extend(self):
        """Extend the model if needed.
        
        This method is called after the copy of the new field.  That means
        that it is connected to a model (self.model points to a class,
        not to None) and you can use this instance attribute to extend
        the class.
        
        """
        pass
    
    def accept_value(self, value):
        """Return wether this field type accept the specified value.
        
        For instance, a string field type will accept str Python type.
        
        Raise a ValueError if the value is not supported.
        
        """
        raise ValueError("invalid value {} for {}.{}".format(repr(value),
                repr(self.model), self.field_name))

class Integer(BaseType):
    
    """Field type: integer.
    
    This type of field handle an integer (positive, null or negative).  It
    DOES NOT handle floating numbers (see Float below).
    
    """
    
    type_name = "integer"
    def __init__(self, pkey=False, auto_increment=False, default=None):
        BaseType.__init__(self, pkey, default)
        self.auto_increment = auto_increment
    
    def accept_value(self, value):
        """Return True if this value is accepted.
        
        Raise a ValueError otherwise.
        
        """
        if value is not None and not isinstance(value, int):
            BaseType.accept_value(self, value)
        
        return True

class String(BaseType):
    
    """Field type: string.
    
    This type of field handles a string of characters of different length.
    
    """
    
    type_name = "string"
    def __init__(self, pkey=False, default=None):
        BaseType.__init__(self, pkey, default)
    
    def accept_value(self, value):
        """Return True if this value is accepted.
        
        Raise a ValueError otherwise.
        
        """
        if not isinstance(value, str):
            BaseType.accept_value(self, value)
        
        return True

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
