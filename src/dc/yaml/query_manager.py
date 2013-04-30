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


"""Module defining the YAMLQueryManager class, defined below."""

from dc.query_manager import QueryManager
from model.functions import *

class YAMLQueryManager(QueryManager):

    """Class representing the YAML query manager, used to interpret queries.

    The YAMLConnector is somehow peculiar, since it is not by default
    connected with a system to query the stored datas.  The query
    manager defined here just works with the cashed objects, because
    YAML fills the cash when launched and stores the cached objects
    in file when closed.  Therefore, every manipulated model object
    should be accessible in the cache and the cache itself could be
    queried to get some specific results.

    The queries are therefore converted into Python code.

    BEWARE: the query manager for the YAML data connector is not
    really fast.  If yoy have not too many lines, it should run
    without problems.  But as the number of data increases, another
    connector should be prefered, primarily (but not only) because
    the query manager of this connector has to browse EVERY SINGLE
    object to get a result.

    """

    @staticmethod
    def equal(field, value):
        """Simply return the equal comparison."""
        return field == value

    @staticmethod
    def notequal(field, value):
        """Simply return the not equal comparison."""
        return field != value

    @staticmethod
    def lowerthan(field, value):
        """Simply return the lower than comparison."""
        return field < value

    @staticmethod
    def lowerequal(field, value):
        """Simply return the lower equal comparison."""
        return field <= value

    def find_operator(self, operator):
        """Return a function used to compare datas."""
        operators = {
            "=": self.equal,
            "!=": self.notequal,
            "<": self.lowerthan,
            "<=": self.lowerequal,
        }

        return operators[operator]

    def query_objects(self, query):
        """Look for the specified objects."""
        model = query.first_model
        name = get_name(model)
        objects = list(self.repository_manager.objects_tree.get(
                name, {}).values())

        # Add simple filters
        for filter in query.filters:
            function = self.find_operator(filter.operator.name)
            field = filter.field
            parameters = self.get_parameters_for_filter(filter)
            objects = [model_object for model_object in objects if \
                    function(getattr(model_object, field), *parameters)]

        return objects
