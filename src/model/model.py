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


"""This module defines the Model class, described below."""

from collections import OrderedDict

from model.functions import *
from model.meta import MetaModel
from model.types import *

class Model(metaclass=MetaModel):
    
    """Abstract class for a model.
    
    Each model must inherit from it.  This class provides:
    -   Methods to create, update and delete objects
    -   Methods to find and filter objects.
    
    The Model class use a DataConnector object to access datas (read and write
    it).
    
    Each column is defined in the class body.  For isntance:
    >>> class User(Model):
    ...     '''A model for an user.'''
    ...     username = String(max_size=30)
    ...     password = String(max_size=255)  # hashed password
    ...     creation_date = Datetime()
    ... 
    
    The 'get_fields' function gives a list of the defined attributes:
    >>> get_fields(User)
    ... [<field 'username'>, <field 'password'>, <field 'creation_date'>]
    
    Class methods:
        build(**attributes) -- create (but don't save) a new object
        get_all() -- return all model's objects
        find(identifiers) -- get an object through its identifiers
        filter(...) -- retrieve one or more object
    
    """
    
    data_connector = None
    bundle = None
    
    # Default fields
    id = Integer(pkey=True, auto_increment=True)
    
    # Class methods
    @classmethod
    def build(cls, **kwargs):
        """Create and return an object.
        
        The created object WILL NOT be saved through the data connector.
        
        """
        new_object = cls()
        fields = get_fields(cls)
        fields = dict((field.field_name, field) for field in fields)
        for name, value in kwargs.items():
            object.__setattr__(new_object, name, value)
        
        return new_object
    
    @classmethod
    def get_all(cls):
        """Return the full list of model's objects."""
        if Model.data_connector:
            with Model.data_connector.u_lock:
                return Model.data_connector.get_all_objects(cls)
        
        return []
    
    @classmethod
    def find(cls, pkey=None, **kwargs):
        """Find and return (if found) an object.
        
        The positional argument, if set, represents the only primary
        key for this object.  This syntax is only allowed if the defined
        model has ONLY ONE primary key.  For instance, by default, it
        has one primary key:  the id.  The syntax:
        >>> Model.find(5)
        would be equivalent to:
        >>> Model.find(id=5)
        The fist syntax, though, is accepted if the model defines only
        one primary key.  Otherwise, the specified matching values could
        be specified in named arguments:
        >>> model.find(ref='AIX032', year=2012)
        
        You cannot use the 'find' method tu search for an object via
        non-primary key fields.  See the 'filter' method instead.
        
        """
        model_name = get_name(cls)
        pkey_names = get_pkey_names(cls)
        pkey_values = OrderedDict()
        repr_pkey_names = tuple(repr(name) for name in pkey_names)
        if pkey:
            if len(pkey_names) != 1:
                raise ValueError("find method called with one positonal " \
                        "argument whereas {} named arguments should be " \
                        "specified: {}".format(len(pkey_names),
                        ", ".join(repr_pkey_names)))
            
            pkey_values[pkey_names[0]] = pkey
        else:
            for name, value in kwargs.items():
                if name not in pkey_names:
                    raise ValueError("the field name {} is not a primary " \
                            "key field of the model {}".format(
                            repr(name), model_name))
                
                pkey_values[name] = value
            
            if len(pkey_values) != len(pkey_names):
                raise ValueError("not all primary key fields were " \
                        "specified for the model {}, expects {}".format(
                        model_name, ", ".join(repr_pkey_names)))
        
        object = None
        with Model.data_connector.u_lock:
            object =Model.data_connector.find_object(cls, pkey_values)
        
        return object
    
    def __init__(self, **kwargs):
        """Create an object from keyword parameters.
        
        This method SHOULD NOT be redefined in a subclass.
        
        """
        fields = get_fields(type(self))
        fields = dict((field.field_name, field) for field in fields)
        for name, value in kwargs.items():
            object.__setattr__(self, name, value)
        
        # Get the default values
        if kwargs:
            for name, field in fields.items():
                if not field.auto_increment and not name in kwargs and \
                        field.set_default:
                    default = field.default
                    if default is None:
                        raise ValueError("the field {} of model {} has no " \
                                "default value".format(field.field_name,
                                type(self)))
                    elif callable(default):
                        default = default(self)

                    object.__setattr__(self, name, default)
        
        # If named parameters were specified, save the object
        if kwargs and Model.data_connector:
            with Model.data_connector.u_lock:
                Model.data_connector.add_object(self)
    
    def __repr__(self):
        pkeys = get_pkey_values(self)
        pkeys = [repr(field) for field in pkeys]
        pkeys = " ".join(pkeys)
        return "<model {} ({})>".format(get_name(type(self)), pkeys)
    
    def __setattr__(self, attr, value):
        """Set the value to the field.
        
        This method checks the value type as well.
        
        """
        field = getattr(type(self), attr)
        if isinstance(field, BaseType) and field.register:
            # Check the value type
            check = field.accept_value(value)
        
        old_value = getattr(self, attr)
        object.__setattr__(self, attr, value)
        if isinstance(old_value, BaseType):
            # Not set yet
            old_value = None
        
        if field.register and Model.data_connector and \
                Model.data_connector.running:
            with Model.data_connector.u_lock:
                Model.data_connector.update_object(self, attr, old_value)
    
    def delete(self):
        """Destroy the created object.
        
        BEWARE: if the data connector is still up, the object will
        be erased from the database.
        
        """
        if Model.data_connector:
            with Model.data_connector.u_lock:
                Model.data_connector.remove_object(self)
    
    # Methods to represent objects
    def display_representation(self, filters=None):
        """Return a dict containing the filtered self.__dict__."""
        attrs = OrderedDict()
        for field in get_fields(type(self)):
            name = field.field_name
            value = getattr(self, name)
            attrs[name] = value
        
        if filters is None:
            return attrs
        elif isinstance(filters, list):
            filter_attrs = OrderedDict()
            for attr in filters:
                if attr in attrs:
                    filter_attrs[attr] = attrs[attr]
            return filter_attrs
