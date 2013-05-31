.. Python Aboard installation process

Installing
==========

By now, no packaged version of the Python Aboard exists.  As a matter
of fact, you need to download the source code from Github.  Plus,
Python Aboard is still a Proof of Concept (3rd version, with a lot of
possibilites, as you will see).

Installing Python
-----------------

You need first to download and install the
`Python version 3.3 <http://www.python.org/download/releases/3.3.1/>`_.

Note: if you have to compile the Python release from source (could be
necessary on Linux), be sure to have a support for open-ssl activated
when you execute the ./configure command.

Downloading the Python Aboard's source code
-------------------------------------------

Next, you need to download the Python Aboard's source code.  If you have
`Git <http://git-scm.com/>`_ already installed, you need to enter the
following command:

    git clone https://github.com/v-legoff/pa-poc3.git

Installing dependencies
-----------------------

Python Aboard needs several dependencies.  You may install them directly
using the scripts in src/tools:

* First run with Python 3.3 the distribute_setup.py which should install the
  'distribute' package
* Then execute dependencies.py which should install the required
  dependencies.  As this script uses the 'distribute' module, it should
  have been installed first.

This script will ask you if you want pymongo and py-postgresql.  These two
modules are only needed if you want to store your data in a MongoDB database
or if you want to store them with PotgreSQL.  You don't need either of them
if you wish to use sqlite3 or yaml data connector.

Note: you can also build a virtual environment to install Python Aboard
dependencies.  This has been tested under a Linux Gentoo and works perfectly
well.
