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


import os

"""Module containing generic opetating system functions to copy."""

def copydir(source, destination, **variables):
    """This function should be used to recursively copy a directory's content.

    The source's content is copied into the destination.  Files are
    copied with 'copyfile', directories are created and recurisvely
    copied using this same function.

    Variables are used to copy the file's content using the
    'str.format' method.

    """
    for name in os.listdir(source):
        source_node = os.path.join(source, name)
        destination_node = os.path.join(destination, name)
        if os.path.isfile(source_node):
            copyfile(source_node, destination_node, **variables)
        elif os.path.isdir(source_node):
            if not os.path.exists(destination_node):
                os.makedirs(destination_node)

            copydir(source_node, destination_node, **variables)

def copyfile(source, destination, **variables):
    """Copy the file from source to destination.

    The content of the source file is read and formatted using
    'str.format' with the specified variables.

    """
    with open(source, "r") as source_file:
        content = source_file.read()
        content = content.format(**variables)

    with open(destination, "w") as destination_file:
        destination_file.write(content)
