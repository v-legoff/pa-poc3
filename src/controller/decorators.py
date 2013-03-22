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


"""This module contains decorators useful for the controller.

Provided decorators:
    model_id -- convert the positional arguments into model objects

"""

def model_id(*names_of_model):
    """Decorator which takes integers and convert to object.

    The number of arguments should match the number of positional
    arguments expected by the callable (the method controller).

    If, for instance, the controler method is like that:
    >>> def view(self, user):
    Then the line just above should be something like:
    >>> @model_id("user.User")

    """
    def decorator(function):
        """Main wrapper."""
        def callable_wrapper(controller, *args, **kwargs):
            """Wrapper of the controller."""
            # Convert the list of arguments
            c_args = []
            for i, arg in enumerate(args):
                model_name = names_of_model[i]
                if model_name:
                    # Get the model
                    model = controller.server.get_model(model_name)
                    try:
                        object = model.find(arg)
                    except ObjectNotFound as err:
                        return str(err)

                    c_args.append(object)
                else:
                    c_args.append(arg)

            return function(controller, *c_args, **kwargs)
        return callable_wrapper
    return decorator
