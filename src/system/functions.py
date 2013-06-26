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


"""Module containing generic operating system functions.

Functions defined in this module:
    get_executable_command -- return the command used to launch PA

"""

import os
import sys

def get_source_directory():
    """Return the source or built (executable) directory.

    """
    # If the first argument if sys.argv ends with a .py
    if sys.argv[0].endswith(".py") or "PythonService" in sys.argv[0]:
        source_directory = os.path.abspath(os.path.dirname(__file__) + "/..")
    else:
        source_directory = os.path.dirname(sys.executable)

    return source_directory

def get_executable_command():
    """Return the command used to launch Python.

    If Python Aboard is launched from source, it will be something like:
        'C:\\python33\\python.exe C:\\path\\to\\src\\aboard.py'
    Or:
        '/usr/local/bin/python3.3 /path/to/src/aboard.py'

    """
    executable = sys.executable
    source = get_source_directory()
    if os.path.basename(executable).lower() in ("python", "python.exe"):
        executable += " " + os.path.join(source, "aboard.py")
    elif os.path.basename(executable) == "winservice.exe":
        executable = os.path.join(source, "aboard")
        if not os.path.exists(executable):
            executable += ".exe"
    elif "PythonService" in executable:
        executable = os.path.abspath(executable + "/../../../../python")
        if not os.path.exists(executable):
            executable += ".exe"

        executable += " " + os.path.join(source, "aboard.py")

    return executable
