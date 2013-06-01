.. Project structure

Project structure
=================

Before starting to use Python Aboard, you need to understand how it
works.  Python Aboard is, in itself, a software which comes with a
stable and secured HTTP server.  It can run one or several web sites.
But Python Aboard doesn't contain your web site definition, of course.

Your web site definition is contained in "a Python Aboard project".  A
project is simply a directory containing your configuration.  Note that
"configuration" is used very extensively:  your task as a Python Aboard
user won't be to create some configuration files and have a complex
web site.  The "user configuration" also contains Python files that
will be used to describe more complex behaviors.  But we'll tak about
that later.

For now, just remember:  a Python Aboard's project is a directory
containing other directories and some files.  We will see shortly what
is stored in this directory.

Now, when you launch Python Aboard, you will ask it to "load" your
user configuration (stored in the project's directory).  Python Aboard
will read this configuration, load the Python files and execute them if
needed and build a full web site with it.

Python Aboard's main executable
-------------------------------

Remember:  Python Aboard is a software.  You will execute it to manage
your project.  As we are, for now, using the source files directly, you
need to launch "src/aboard.py" with Python 3.3.

First, you need to open a console.  Under Linux I don't think you will have
much trouble doing it.  Under Windows, you have to find the command-line.
One of the way is to open the "Execute" menu (you can press Windows + R),
enter "cmd" and press return.

Then you need to launch the Python Aboard's main executable::

    # Under Linux it may be something like that
    python3.3 ~/pa-poc3/src/aboard.py

    # And under Windows
    c:\python33\python.exe C:\users\user\pa-poc3\src\aboard.py

Yes, Under Windows, it's a somewhat longer command but there are ways to
shorten it with some configuration, out of the scope of this tutorial.

If everything works, you should get a reminder of the Python Aboard's commands::

    Python Aboard Command Line

    Use one of the following sub-command:
        list - list specific informations
        create - create new things
        start - start a process

The Python Aboard's executable expects some kind of action.  By now,
create, list or start.  Here we want to create a new project.

Creating a new project
----------------------

We're going to use the "create project" command.  It takes only one
parameter:  the project's name that will be the newly created directory's
name, as well.

Note: for now on, I'll skip the complete command used to launch the
Python Aboard's main executable.  Remember to use the full command::

    > aboard.py create project try-pa
    done

The tool is not very talkitive, but it created a directory called
"try-pa".  You can open it.  It should contain the following sub-directories:

* "bundles": the directory that will contain the project's bundles (details
  below).
* "config": the directory containing the standard project configuration.
  Mostly, in it's one of the configuration files that you will specify
  the hostname and port of your web server.
* "layout": this directory contains the general structure of your pages.
  This structure is used by the templating system and we will comeback
  to it in this tutorial.
* "plugins": this directory contains plugins used to extend the Python
  Aboard's functionalities.  This directory will remain empty for us
  during this tutorial, but the process of installing and using
  plugins is described in the full documentation.
* "static": this directory contains the static files of your project.  If
  you want to store images, sounds or other files that are static, it's
  where they will be stored.  Well, perhaps, that's something we will
  discuss in greater details.

The Python Aboard's main executable created the basic structure of
the project and we will use it in the next sections of this tutorial.  But
we can do something already...

Starting the web server
-----------------------

Starting our web server is simple.  we will use one of the command of
the Python Aboard's main executable.  But first we have to move to the
"try-pa" directory that has been created by the "create project"
command::

    > cd try-pa
    > aboard.py start server

One more time, remember to use the full command to launch the Python
Aboard's main executable.  After entering the "start server" command,
you should see some messages like this::

    [31/May/2013:14:11:36] ENGINE Listening for SIGTERM.
    [31/May/2013:14:11:36] ENGINE Bus STARTING
    [31/May/2013:14:11:36] ENGINE Set handler for console events.
    [31/May/2013:14:11:36] ENGINE Started monitor thread '_TimeoutMonitor'.
    [31/May/2013:14:11:36] ENGINE Serving on 127.0.0.1:9000
    [31/May/2013:14:11:36] ENGINE Bus STARTED

You can try to connect to it:  in your favorite web browser, enter
the address `<http://localhost:9000/>`_ and watch...

A 404 error!

The web page cannot be found and that's not that strange, since we created
a new project... with nothing in it.  That means no page exist yet.  We'll
learn how to do it in the next section.

To shutdown the web server, just press CTRL + C.  You could have to wait
some time, since shutting down implies a lot of process (much more than
running the web server in the first place, as a matter of fact).
