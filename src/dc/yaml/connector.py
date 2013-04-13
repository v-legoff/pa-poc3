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


"""Module defining the YAMLConnector class."""

import os

driver = True

try:
    import yaml
except ImportError:
    driver = False

from dc.connector import DataConnector
from dc import exceptions
from dc.yaml.configuration import YAMLConfiguration
from dc.yaml.driver import YAMLDriver
from dc.yaml.query_manager import YAMLQueryManager
from dc.yaml.repository_manager import YAMLRepositoryManager
from model import exceptions as mod_exceptions
from model.functions import *

class YAMLConnector(DataConnector):

    """Data connector for YAML.

    This data connector should read and write datas in YML format, using
    the yaml library.

    A very short example:
        # Table: users
        - id: 1
          username: admin
          email_address: admin@python-aboard.org

    """

    name = "yaml"
    configuration = YAMLConfiguration
    driver = YAMLDriver
    query_manager = YAMLQueryManager
    repository_manager = YAMLRepositoryManager
