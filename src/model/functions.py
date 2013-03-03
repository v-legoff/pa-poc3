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


"""This module contains different useful functions for manipulating models.

Functions defined here:
    get_fields(class) -- return the class's field
    get_name(class) -- return the model's name
    get_plural_name(class) -- return the plural class name
    get_pkey_names -- return a list of primary key fields name
    get_pkey_values -- return a list of primary key fields values
    update_attr -- update an object attribute
    update -- update a whole object

"""

from model.types import BaseType

def get_fields(model, register=False):
    """Return a list of the defined fields in this model.
    
    If register is True, only return the fields that can be registered (not
    the relations).
    
    """
    fields = [getattr(model, name) for name in dir(model)]
    fields = [field for field in fields if isinstance(field, BaseType)]
    fields = sorted(fields, key=lambda field: field.nid)
    if register:
        fields = [field for field in fields if field.register]
    
    return fields

def get_fields_values(object, register=False):
    """Return a dictionary containing the object's fields and values.
    
    The dictionary as the field's names as keys and the fiel's values as
    values.
    If the 'register' parameter is set to True, only the fields "to be
    registered" are set.
    
    """
    fields = get_fields(type(object))
    dict_fields = {}
    for field in fields:
        if register and not field.register:
            continue
        
        value = getattr(object, field.field_name)
        dict_fields[field.field_name] = value
    
    return dict_fields

def get_name(model, bundle=True, lower=False):
    """Return the model name.
    
    If bundle is True, include the bundle's name.
    If lower is True, the name is lowercased.
    
    """
    name = model.__name__
    name = name.split(".")[-1]
    if bundle and model.bundle:
        bundle_name = model.bundle.name
        name = bundle_name + "." + name
    
    if lower:
        name = name.lower()
    
    return name

def get_plural_name(model):
    """Return the plural model's name.
    
    The plural name is:
        The value of the 'plural_name' class attribute if exists
        The singular name extended with the 's / es' rule otherwise
    
    """
    if hasattr(model, "plural_name"):
        return model.plural_name
    else:
        singular_name = get_name(model, bundle=False, lower=True)
        if singular_name.endswith("y"):
            singular_name = singular_name[:-1] + "ies"
        elif singular_name.endswith("s"):
            singular_name += "es"
        else:
            singular_name += "s"
        
        return singular_name

def get_pkey_names(model):
    """Return a list of field names (those defined as primary key)."""
    fields = get_fields(model)
    p_fields = [field.field_name for field in fields if field.pkey]
    return p_fields

def get_pkey_values(object, replacement=None):
    """Return a tuple of datas (those defined as primary key).
    
    If specified, the replacement should be a dictionary with
    {name: value} to replace the values of certain attributes.
    
    NOTE: the 'get_pkeys_name' function expects a model as argument
    (a class).  This function, however, expects an object created on a
    Model class.
    
    """
    if replacement is None:
        replacement = {}
    
    fields = get_fields(type(object))
    p_fields = [field.field_name for field in fields if field.pkey]
    values = []
    for attr in p_fields:
        if attr in replacement:
            value = replacement[attr]
        else:
            value = getattr(object, attr)
        values.append(value)
    
    return tuple(values)

def update_attr(to_update, attribute, value):
    """Update the object passed as first argument.
    
    NOTE: this function is really close to 'setattr' but it only writes
    the new attribute in the object, without calling its '__setattr__'
    magic method, which is useful for a model if you don't want to
    update it in the data connector.
    
    """
    object.__setattr__(to_update, attribute, value)

def update(to_update, dict_of_values):
    """Update the attributes of an object using update_attr."""
    for name, value in dict_of_values.items():
        update_attr(to_update, name, value)

def is_built(object):
    """Return whether the object is built or not.
    
    An object is build if its field attributes are not BaseType.
    
    """
    fields = get_fields(type(object))
    values = [getattr(object, field.field_name) for field in fields]
    bases = [isinstance(field, BaseType) for field in values]
    return not any(bases)
