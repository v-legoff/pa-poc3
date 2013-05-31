.. Python Aboard introduction

Brief introduction to Python Aboard
===================================

What is Python Aboard?
----------------------

Python Aboard is a web framework built with Python 3.3.  It allows a user
to create one (or more) website(s) with a simple configuration and some
simple files of code.  Simple, yet powerful, Python Aboard can be
extended through different plugins.  Furthermore, the website
components (called bundles) can be distributed and
re-used by other users to easily create a rich website without
coding everything inside it.

Python Aboard:

* Is provided with an advanced HTTP server courtesy of `CherryPy
  <http://www.cherrypy.org/>`_.
* Is highly configurable with a simple `YAML syntax
  <http://yaml.org/spec/1.1/#id857168>`_.
* Can store and retrieve datas using different drivers that are called
  'data connectors' in the project.  The most simple data connector is
  called 'yaml' and stores the datas in a `YAML format
  <http://yaml.org/spec/1.1/#id857168>`_.
* Uses the `MVC (Model-View-Controller)
  <en.wikipedia.org/wiki/Model–view–controller>`_ principles.
* Divides a website into 'bundles' of code and configuration allowing
  a greater distribution of website components.
* Proposes a templating language, courtesy of
  `Jinja2 <http://jinja.pocoo.org/docs/>`_, that makes the writing of
  HTML pages (and other formats) pretty easy.

This features will be presented by this tutorial.  Some more detailed
explanations can be found on :doc:`/documentation/index`.

What will this tutorial allow me to do?
------------------------------------

This tutrial will help you:

* Learn to install Python Aboard.
* Configure your first website and get your first basic dynamic pages.
* Create your first models (data to store).
* Create your first views with the templating language.
* Setup your controllers to bring everything together.

At the end of this tutorial, you should have a working website with
a simple blog.  Note, however, that you should try directly the given
code and examples and even work on the enhancement proposals that
are given on almost every page.

What will I need to learn?
--------------------------

Python Aboard is designed to be both very simple for beginners and
very powerful for advanced users.  Therefore, to read this tutorial,
you shouldn't need a lot of knowledges.

However, it is required for you to know, even basically, the
`HTML language <http://www.w3schools.com/html/>`_ that is used to describe
web pages.  You shouldn't need to know the `CSS language
<http://www.w3schools.com/css/>`_ that is used to write style-sheets for
your web page or the `JavaScript language
<http://en.wikipedia.org/wiki/JavaScript>`_ that is used to create dynamic
pages on the client's side, but both languages may be very useful.

Furthermore, remember that Python Aboard is written in `Python
<http://www.python.org/>`_.  The user's website is partly designed with
Python code, though, and even if it will remain very simple in this
tutorial, it is really a good idea to learn Python if it's not already done.

Here are some resources:

* `Learn HTML with the W3Schools <http://www.w3schools.com/html/>`_.
* `Learn CSS with the W3Schools <http://www.w3schools.com/css/>`_.
* `Learn Python with the official tutorial
  <http://docs.python.org/3/tutorial/index.html>`_.