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

This class contains the user_provider service, specifically used to
retrieve users.  This service also handles the creation or retrieving of
the 'anonymous' user.

"""

from model.exceptions import ObjectNotFound
from service import Service

class UserProviderService(Service):

    """Class containing the user_provider service.

    This service is used to:
    *  Retrieve already created users stored in the data connector
    *  Retrieve (or create if needed) the anonymous user.

    Required configuration informations:
        model_name -- the model's name containing the users
        method_to_retrieve -- method used to retrieve users

    Methods you can use:
        find_user -- find an user

    """

    name = "user_provider"
    model_name = "user.User"
    method_to_retrieve = "find"

    def find_user(self, key):
        """Return the found users or None if no one found."""
        data_connector = self.services.data_connector
        try:
            model = data_connector.get_model(self.model_name)
        except KeyError:
            return None

        try:
            method = getattr(model, self.method_to_retrieve)
            user = method(key)
        except ObjectNotFound:
            return None

        return user
