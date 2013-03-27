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


"""Module containing the DataConnectorService class.

This class contains the data_connector service, used to
manipulate the configured data connector.  It should only perform generic
actions (actions that are common to EVERY defined data connectors).

"""

from service import Service

class DataConnectorService(Service):

    """Class containing the data_connector service.

    This service is basically used to manipulate the defined data
    connector.  It can be used when a data connector has been configured.
    The Python Aboard's server automatically configure this service,
    but if you don't want to use the server at all, you should do
    something like:
    >>> # Import a data connector (here the YAMLConnector)
    >>> from dc.yaml.connector import YAMLConnector
    >>> data_connector = YAMLConnector()
    >>> data_connector.setup(location="~/aboard")
    >>> # Import the service manager
    >>> from service import manager
    >>> manager.load_default_services()
    >>> manager["data_connector"].data_connector = data_connector

    """

    name = "data_connector"
    data_connector = None

    def get_model(self, model_name):
        """Return, if found, the model.

        The name should be "bundle.model" like "blog.Post".
        If the model cannot be found, a KeyError exception will be raised.

        """
        return self.data_connector.models[model_name]
