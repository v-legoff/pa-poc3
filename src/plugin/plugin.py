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


"""Module containing the abstract Plugin class."""

class Plugin:
    
    """Parent class for all plugins.
    
    To create a plugin, a user must inherit from this class.  A
    plugin is a set of code which is designed to extend the abilities
    of the Python Aboard framework, by using other libraries for
    instance.
    
    In order to modify the behaviour of Python Aboard, a plugin uses
    events:  it can subscribe to listen and be called when a specific
    action occurs.  For instance, a plugin could be called any time
    a request is sent to the server.
    
    The 'subscribe_to' class attribute is a tuple containing the names
    of the events to which this plugin is subscribed.  When the event
    occurs, Python Aboard automatically calls each plugin subscribed
    to this event and use the event's name as a method.  If, for
    instance, a plugin is subscribed to the 'extend_server_configuration'
    event, it should have a 'extend_server_configuration' class
    method defined.
    
    """
    
    manager = None
    subscribe_to = ()
    
    @classmethod
    def subscribe(cls):
        """Subscribe the plugin.
        
        This method is called when the plugin is loaded by the plugin
        manager.  It should not be defined in a inherited class.
        
        """
        if cls.manager is None:
            raise ValueError("try to subscribe a plugin without manager")
        
        for event_name in cls.subscribe_to:
            cls.manager.subscribe(cls, event_name)
