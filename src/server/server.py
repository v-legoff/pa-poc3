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


"""Module containg the Python Aboard server, build on CherryPy."""

import hashlib
import os
import sys

import cherrypy
from cherrypy._cptools import HandlerTool
import yaml

from autoloader import AutoLoader
from bundle import Bundle
from configuration.default import *
from controller import Controller
from dc import connectors
from formatters import formats
from formatters.base import Formatter
from model import Model
from plugin.manager import PluginManager
from router.dispatcher import AboardDispatcher
from server.plugins.reloader import Reloader
from service import manager
from templating import Jinja2

class Server:

    """Wrapper of a cherrypy server."""

    def __init__(self, user_directory, check_dir=True):
        self.host = "127.0.0.1"
        self.port = 9000
        self.forwarding_port = None
        self.hostname = "localhost"
        if check_dir:
            self.user_directory = self.check_directory(user_directory)
        else:
            self.user_directory = user_directory

        self.cp_config = {}
        self.dispatcher = AboardDispatcher()
        self.loader = AutoLoader(self)
        self.bundles = {}
        self.configurations = {}
        self.plugin_manager = PluginManager(self)
        self.services = manager
        self.services.register_defaults()
        self.source_directory = ""
        self.templating_system = Jinja2(self)
        self.templating_system.setup()

        Controller.server = self
        Formatter.server = self

    @property
    def models(self):
        """Return all the models."""
        models = []
        for bundle in self.bundles.values():
            models.extend(list(bundle.models.values()))

        return models

    def check_directory(self, directory):
        """Check whether the directory is correct.

        A directory is not correct if:
            It doesn't exist (surprising, hu?)
            It doesn't contain the right repositories and files

        """
        directories = (
            "bundles",
            "config",
            "layout",
        )

        if not os.path.exists(directory):
            raise ValueError("the directory {} doesn't exist".format(
                    directory))

        existing_dirs = [name for name in os.listdir(directory) if \
                os.path.isdir(directory + os.sep + name)]
        for required_dir in directories:
            if required_dir not in existing_dirs:
                raise RuntimeError("the {} directory doesn't exist in " \
                        "{}".format(repr(required_dir), directory))

        abs_directory = os.path.abspath(directory)
        sys.path.append(abs_directory)
        return abs_directory

    def load_configurations(self):
        """This method reads the configuration files found in /config."""
        path = os.path.join(self.user_directory, "config")
        configurations = {
            "data_connector": DataConnectorConfiguration,
            "formats": FormatsConfiguration,
            "server": ServerConfiguration,
        }

        for filename, configuration in configurations.items():
            config_path = os.path.join(path, filename + ".yml")
            configuration = configuration.read_YAML(config_path)
            self.configurations[filename] = configuration

    def prepare(self):
        """Prepare the server."""
        # Update the server's host and port
        if "server" in self.configurations:
            server = self.configurations["server"]
            if "host" in server:
                self.host = server["host"]
            if "port" in server:
                self.port = server["port"]
            if "hostname" in server:
                self.hostname = server["hostname"]
            if "forwarding_port" in server:
                self.forwarding_port = server["forwarding_port"]

        # DataConnector configuration
        dc_conf = self.configurations["data_connector"].datas
        dc_name = dc_conf["dc_name"]
        dc_spec = dict(dc_conf)
        del dc_spec["dc_name"]
        try:
            dc = connectors[dc_name]
        except KeyError:
            print("Unknown data connector {}".format(dc_name))
            return

        dc = dc()
        config_path = os.path.join(self.user_directory, "config",
                "data_connector.yml")
        dc.setup(config_path)
        Model.data_connector = dc
        self.services.services["data_connector"].data_connector = dc

        if "formats" not in self.configurations:
            return
        cfg_formats = self.configurations["formats"]

        # Setup the default_format
        default = cfg_formats["default_format"].lower()
        if default not in formats:
            raise ValueError("unknown format {}".format(default))

        allowed_formats = []
        for format in cfg_formats.get("allowed_formats", []):
            format = format.lower()
            if format not in formats:
                raise ValueError("unknown format {}".format(format))

            allowed_formats.append(format)

        self.data_connector = dc
        self.default_format = default
        self.allowed_formats = allowed_formats
        self.loader.add_default_rules()

    def load_bundles(self):
        """Load the user's bundles."""
        path = os.path.join(self.user_directory, "bundles")
        for name in os.listdir(path):
            if not name.startswith("__") and os.path.isdir(path + "/" + name):
                bundle = Bundle(self, name)
                self.bundles[name] = bundle
        for bundle in self.bundles.values():
            bundle.setup(self, self.loader)

        for model in self.models:
            type(model).extend(model)
        for model in self.models:
            self.data_connector.repository_manager.add_model(model)

    def run(self):
        """Run the server."""
        cherrypy.engine.autoreload.unsubscribe()
        if hasattr(cherrypy.engine, 'signal_handler'):
            cherrypy.engine.signal_handler.subscribe()
        if hasattr(cherrypy.engine, "console_control_handler"):
            cherrypy.engine.console_control_handler.subscribe()
        #cherrypy.engine.reloader = Reloader(cherrypy.engine)
        #cherrypy.engine.reloader.loader = self.loader
        #cherrypy.engine.reloader.server = self
        #cherrypy.engine.reloader.subscribe()
        cherrypy.config.update({
                'server.socket_host': self.host,
                'server.socket_port': self.port,
                'tools.staticdir.root': self.user_directory,
        })
        cherrypy.config["tools.encode.on"] = True
        cherrypy.config["tools.decode.on"] = True
        config = self.cp_config
        config.update({
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'static',
                'tools.staticdir.content_types': {
                        'ogg': 'application/ogg',
                },
            },
        })

        # Some plugins add configuration
        self.plugin_manager.call("extend_server_configuration", cherrypy.engine, config)
        cherrypy.tree.mount(root=self.dispatcher, config=config)
        self.write_PID()
        cherrypy.engine.start()
        cherrypy.engine.block()
        self.del_PID()

    def get_model(self, name):
        """Try and retrieve a Model class."""
        bundle_name, model_name = name.split(".")
        bundle = self.bundles[bundle_name]
        model = bundle.models[name]
        return model

    def get_repository(self, model_name):
        """Return the repository bound to the specified model.

        The full name ('bundle.Model') should be specified.

        """
        model = self.get_model(model_name)
        return model._repository

    def write_PID(self):
        """Write the PID (os.pid) in the user's directory configuration."""
        path = os.path.join(self.user_directory, "tmp")
        if not os.path.exists(path):
            os.makedirs(path)

        pid = os.getpid()
        pid_path = os.path.join(path, "pid")
        with open(pid_path, "w") as pid_file:
            pid_file.write(str(pid))

    def del_PID(self):
        """Delete the file containing the server's PID."""
        path = os.path.join(self.user_directory, "tmp")
        if os.path.exists(path):
            pid_path = os.path.join(path, "pid")
            os.remove(pid_path)

    def get_cookie(self, name, value=None):
        """Get the cookie and return its value or 'value' if not found."""
        try:
            return cherrypy.request.cookie[name].value
        except KeyError:
            return value

    def set_cookie(self, name, value, max_age, path="/", version=1):
        """Set a cookie."""
        cookie = cherrypy.response.cookie
        cookie[name] = value
        cookie[name]['path'] = path
        cookie[name]['max-age'] = max_age
        cookie[name]['version'] = 1

    def authenticated(self):
        """Return whether the current request is authenticated or not."""
        client_token = self.get_cookie("PA-client-token")
        if not client_token:
            print("no cookie")
            return False

        headers = cherrypy.request.headers
        if "Remote-Addr" not in headers:
            print("no IP")
            return False

        to_hash = "Python-Aboard " + headers.get("Remote-Addr", "none")
        to_hash += " " + headers.get("User-Agent", "unknown")
        to_hash = to_hash.encode()
        token = hashlib.sha256(to_hash).digest()
        return client == client_token
