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


"""This module contains the Table class.

This class is used to represent a Model's structure regarding the used data
connector.  It is not only the name and types of fields defined in a model,
but also describe a table in the data connector (the most simple example
is a table in a database).  That means that Model tables and stored
tables (in a data connector) could be different, and this class should
manage the changes (create new fields, delete old ones, change types...).

"""

from model.functions import *

class Table:
    
    """Class representing a Model table, that is its attributes.
    
    When a Model is registered in a data connector, it:
        Creaates the table (class Table) representing the Model structure
        Creates the table (subclass of Table) representing the storage.
    
    For instance, consider this scenario:
        1.  You create the User model as follow:
            username (string)
            password (string)
        2.  You register this model in the data connector
        3.  You happily record some users in your data connector
        4.  You decide that you will add a new field in your User model:
            email (String)
        5.  Then, when you're User model will be registered in your data
            connector, it will detect that one field (email) is not
            present in your stored table.  It will create it.
    
    This process is data connector independent.  That's why data
    connectors should create their own subclass of Table to handle these
    operations (see the methods below).
    
    Methods defined in this class, some of them may be redefined:
        build -- build the table columns
        add_column -- add a new column
        del_column -- del a column
        change_type_column -- change the type of a column.
    
    To see how these methods are called, see the 'compare_and_fix'
    method.
    
    """
    
    def __init__(self):
        self.columns = ()
    
    def __repr__(self):
        ret = "<table ("
        for m_type in self.columns:
            ret += m_type.field_name + ":" + m_type.type_name
        
        ret += ")>"
        return ret
    
    def build(self, model):
        """Build the table columns.
        
        This method uses model (subclass of Model) but data connectors
        who inherit this class may use different types, like a string.
        
        """
        self.columns = tuple(get_fields(model))
    
    def compare_and_fix(self, other):
        """This method should be called to detect changes between tables.
        
        Its job is to:
        *  Detect these changes
        *  Fix them.
        
        The 'self' table is still considered "the referrence".  If something
        is wrong, it's in the second table.  Be careful,
        table1.compare_and_fix(table2) will not do the same thing as
        table2.compare_and_fix(table1).
        
        """
        # We should browse the tables content with a while loop
        i = 0
        while i < max(len(self.columns), len(other.columns)):
            try:
                col1 = self.columns[i]
            except IndexError:
                # Should delete the second one
                col2 = other.columns[i]
                other.del_column(col2)
                break
            
            try:
                col2 = other.columns[i]
            except IndexError:
                # The column doesn't exist in the other table, creates it
                other.add_column(col1)
                break
            
            # Now we have col1 (from self) and col2 (from other)
            # Are they the same ones?
            if col1.field_name != col2.field_name:
                # Try to find col1 in the other table, somewhere else
                # If it's there, then move it from its old place
                # Otherwise, creates it.
            
            # col1 and col2 describes the same field, but do they match?
            # Have they the same type?
