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


"""This file contains the DataConnector class, defined below."""

import os
import yaml

class DataConnector:

    """Class representing a data connector, a wrapper to access datas.

    The Data Connector is a class that contains:
    -   A Driver, used to communicate with the data storage
    -   A repository manager, used to manage the objects and the cache
    -   A query manager, used to interpret queries.

    """

    name = "unspecified"
    configuration = None
    driver = None
    query_manager = None
    repository_manager = None
    def __init__(self):
        """Initialize the data connector."""
        self.driver = type(self).driver()
        self.repository_manager = type(self).repository_manager(self.driver)
        self.query_manager = type(self).query_manager(self.driver,
                self.repository_manager)

    @property
    def u_lock(self):
        return self.driver.u_lock

    def setup(self, configuration_path):
        """Try to setup and open the data connector."""
        config = type(self).configuration
        configuration = config.read_YAML(configuration_path)
        self.driver.open(configuration)

    def setup_test(self):
        """Setup for testing."""
        path = "tests/config/dc/" + type(self).name + ".yml"
        self.setup(path)
