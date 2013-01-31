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


"""Module containing the UserProviderService class.

This class contains the user_provider service, originally used to
link an access token to a valid user, if it is possible.  This
service is highly customizable and can find other informations
than users, as well as receive something else than tokens.

"""

import time

from model.exceptions import ObjectNotFound
from service import Service

class AuthenticationService(Service):
    
    """Class containing the authentication service.
    
    This service is basically used to easily manage and store access
    tokens.  Thus, it can be used to request that a 'user' be
    'logged in' in order to continue.
    
    This service DOES NOT manage users, though.  When it reads and
    validate an access token, it contact another service, the
    'UserProvider', to know what the stored informations on the
    access token line means.
    
    If you want to use this service to keep the same authentication
    method (by client cookies) or even if you want to write a different
    one, just create a service in your bundle that inherits from
    this class and supply some informations:
        token_model -- the name of the access token model
        user_provider -- the name of the service used to retrieve users
        time_expire -- for how many seconds the access token be valid
    
    """
    
    def __init__(self):
        Service.__init__(self)
        self.token_model = ""
        self.user_provider = "user_provider"
        self.time_expire = 900
    
    def authenticated(self, request):
        """Return whether the request has stored a valid access token."""
        value = self.server.get_cookie("python-aboard-auth")
        if not value:
            return False
        
        try:
            Token = self.server.get_model(self.token_model)
        except KeyError:
            return False
        
        try:
            token = Token.find(value=value)
        except ObjectNotFound:
            return False
        
        if token.timestamp + self.time_expire < time.time():
            print("too old")
            return False
        
        try:
            provider = getattr(self.services, self.user_provider)
        except AttributeError as err:
            print(err)
            return False
        
        if hasattr(provider, "from_access_token"):
            provided = provider.from_access_token(token)
        else:
            print("Method not found")
            return False
        
        return provided
    
    def authenticate(self, request, user):
        """Authenticate the user.
        
        This method:
            Create a new token
            Combine the token public value and the remote address
            Store on the client-side (cookie) the value
        
        """
        remote_addr = request.headers["Remote-Addr"]
        Token = self.server.get_model(self.token_model)
        token = Token(user=user.id, timestamp=int(time.time()))
        name = "python-aboard-auth"
        self.server.set_cookie(name, token.value, self.time_expire)
