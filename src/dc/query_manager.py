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


"""Module defining the QueryManager abstract class, defined below."""

from abc import *

from model.functions import *

class QueryManager(metaclass=ABCMeta):

    """Abstract class to represent a query manager for a connector.

    A query manager is a class that is dedicated to interpret generic
    queries (see the 'query' package).  Each data connector should
    implement a query manager and each query manager should interact with the data connector to query
    some informations in the data storage.  For instance, a generic
    query could be converted to a SQL query for a SQL data connector.

    """

    def __init__(self, driver, repository_manager):
        self.driver = driver
        self.repository_manager = repository_manager

    def query_objects(self, query):
        """Return a list of model objects filtered by the query.

        In this method are performed the query convertion to something
        the data connector could understand and use.  The repository
        manager's cache could be used to retrieve the corresponding
        object, but first we have to query for the specific result.
        Therefore, this method should not be redefined in a subclass,
        rather redefine the 'query' method.  Sometimes, though, it could
        be smarter to redefine this method (if you have a data connector
        that only relies on the cache, for instance).

        """
        lines = self.query(query)
        objects = []
        name = get_name(query.first_model)
        for line in lines:
            model_object = self.repository_manager.get_or_build_object(
                    name, line)
            objects.append(model_object)

        return objects

    def query(self, query):
        """Query for the specified query.

        This time, instead of returning objects, we return lines (list of
        list).  This method is, therefore, closer to the driver and
        should not use the Python Aboard's model layer.

        """
        pass
