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


"""This module contains the model listeners.

Listeners are callbacks (generally methods) that will be called in speific contexts.  For instance, a method could be called when a specific object attribute is modified.  A different one could be called when a new object is created, a third when an object is loaded from the database, and so forth.

This module defines a decorator, 'listen', which must be applied to a specific callable in a model class:

>>> from datetime import datetime
>>> from model import *
>>> class BlogPost(Model):
...     '''A glob post.
...
...     The 'last_edited' field is set when the post's content
...     is modified.
...
...     '''
...     title = String()
...     content = String()
...     last_edited = DateTime()
...
...     @listen("post_update", "content")
...     def update_edition(self):
...         '''Called when the content is modified.'''
...         self.last_edited = datetime.now()

This module also defines the 'call_event' function but it should
only be used by the Python Aboard's code or extensions, not directly
by Python Aboard's users.

"""

from model.events import *

def listen(event_name, *args, **kwargs)
    """Decorator to set a model's instance method to listen for some events.

    The expected arguments are different depending on the used
    events.  This decorator should only be used on instance methods
    (neither class methods nor static methods).  You could use this
    decorator several times to listen to different events with the
    same method.

    """
    class_event = EVENTS[event_name]
    event = class_event(*args, **kwargs)
    def decorator(function):
        """Main wrapper."""
        def method_wrapper(model_object, *o_args, **o_kwargs):
            """Wrapper of the controller."""
            return event(function, *o_args, **o_kwargs)
        model = type(function.__self__)
        model._events[event_name] = method_wrapper
        return callable_wrapper
    return decorator

def call_event(model_object, event_name, *args, **kwargs):
    """Call a model event by its name with its arguments."""
    model = type(model_object)
    if event_name in model._events:
        model._events[event_name](model_object, *args, **kwargs)
