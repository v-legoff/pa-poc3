.. From nothing to bundles

From nothing to bundles
=======================

Python Aboard is built around the logic of "bundles".  But exactly what
is it?  What are they for?  What can they do?  I will try to answer these
questions in this section.

What are bundles?
-----------------

Bundles are components of a web site.  For instance, the users are often
managed by one bundle.  If you want to add a board to your web site,
you will most likely create a new bundle dedicated to it.  A chat?  One
more bundle.  Maybe a blog?  Another bundle.

The question is:  why can't I create all my web site as is, without
dividing it in components?  Dividing takes time, after all, and if it's
not worth the trouble, well I'd better use something more simple.

But dividing doesn't take that much time, and if it does, it's much
worth the trouble.  If you have a fairly complicated web site with a
lot of different components, the bundles will be a blessing.  If you have a
small web site that does something, only one thing but do it right, then
you will have your web site logic in one bundle.  And if you want to
extend your web site (by adding new components), you will just install
new bundles.

There is another advantage to divide your web site in bundles:  it's
almost impossible to find similar web sites on the Web, that is web sites
that are built the same way, have the same pages and contain the same
informations.  However, you can find a lot of web sites with similar
components.  After all, thousand of blogs are built on the same model and
that's why `WordPress <http://wordpress.com/>`_ is so popular.

If you create a bundle dedicated to a component of your web site, you may
be able to distribute it.  Other web developers could see your bundle,
install it in their project and have the component you developed
without bothering to develop it themselves.  You could be one of the
developers using existing bundles, or some developer posting new bundles.
Python Aboard WILL have a way to distribute this bundles and find
them very easily.

What does a bundle contain?
---------------------------

As said above, a bundle contains one component of a web site.  Here is a
not exhaustive list of what you could find in a bundle:

* models: models represent datas that are stored on your machine,
  maybe (but maybe not) in a database.
* views: views are templates used to describe the dynamic content of a
  page.  Basically, a template could represent some pages on your site.
* controllers: controllers are functions (or methods, to be more exact)
  that will be called for a certain route and bring everhing together.
* services: services are objects dedicated to something very
  specific.  The most obvious service is used to send e-mails, for instance.
* ...

Don't worry if you don't understand the listed functionalities:  we will
see them one at a time.

-------------------------
Creating our first bundle

Even for a very simple web site, we need at least to create one bundle.
The Python Aboard's main executable has a command to do it:  "create bundle".

You have to execute it in your directory containing the project (that
is, for us, in the "try-pa" directory).  You have to specify a
bundle's name and, for this example, we'll call it simply
"welcome"::

    > aboard.py create bundle welcome
    Bundle 'welcome' created
    A default configuration was set.

Our new bundle was created.  You can check in the "bundles"
sub-directory, you should have a directory called "welcome".  And if
you open it, you will see other files and directories that I will
describe a little later.

This bundle is not empty.  The "create bundle" command told us that
"a default configuration was set" which means that our new bundle
was created with some default files.  Very few of them, as a matter
of fact, but enough to have something to show.

Still in the project's directory, execute the command::

    > aboard.py start server

And go to: `<http://localhost:9000/>`_ like we did in the next section.
But this time, you shouldn't see an error but a real page, short and
somewhat ugly, but working.

What just happened?
^^^^^^^^^^^^^^^^^^^

The "create bundle" command created a default bundle with, for the
user, one page on the root (/) of our web site.  For your web site
users, this means that you can redirect them to the `/
<http://localhost:9000/>`_ page.  For you (or other Python Aboard's
users), it means that a **route** was created.  A route is a link between
an URI (here simply /) and a function.  We will elaborate some more,
but it's what you have to remember for now.

Our only route tells something like:  connect the / address to a
function, let's call it "home", it makes some sense after all.  So
when you connect to `/ <http://localhost:9000/>`_, Python aboard
looks for the right route, finds the one defined in your newly created
bundle and calls the "home" function.

This function is also defined in your bundle.  It's called an
**action** and should return what will be sent to the user's browser
(an HTML page, more often than not).  But the HTML code is not
written in your action, we use a special view that will contains the
HTML code and our action will return this view.

Now let's see the code to achieve this.

The routing configuration
-------------------------

First, we will see how routes are defined.  Go in your bundle directory
"try-pa" -> "bundles" -> "welcome").  The different routes are
configured very easily with a configuration file that you will find in
the "config" sub-directory.

Open it.  You should find the "routing.yml" file.  You can open it
with a standard editor (notepad under Windows, Emacs or Vim under
Linux).  Inside, you should see something like this::

    # Controller: Welcome
    home:
      pattern: /
      controller: welcome.Welcome.home

That's YAML.  You can find useful informations about the syntax on
`the specifications page <http://yaml.org/spec/1.1/#id857168>`_.  On the
other hand, it's not very complicated and the syntax will be
explained when needed.

For now, it's very simple:

#. The first line is a comment (so it's ignored by the parser).
#. The second line is the name of the route.  Here it's called "home"
   but you can choose another name, of course.  Names of route have to
   be unique in a single bundle and we will see why in a moment.
   Notice that this second line ends with a colon.
#. The third line is slightly indented: it starts with two spaces and
   it means that this line refers to the previous block (the second line).
   It contains three elements:

   * The word "pattern"
   * A colon and a space after it
   * The corresponding pattern (here "/")

   If you remember what a route is, this line is the "what URI should
   I watch" part.
#. The fourth line is slighly indented, too, and formed the same way
   as the previous line.  We specify here the controller that will
   be called when a browser asks for the "/" page.  The controller
   definition has three parts separated by dots:

   * The first one is the bundle's name ("welcome").
   * The second one is the controller's name ("Welcome", with a capital "W").
   * The third one is the action's name ("home").

   Controllers and actions will be explained shotly after.

So, as you see, a route has three main parts:

* A unique name inside a bundle (here "home")
* A pattern that tells Python Aboard what URI it should watch (here "/")
* A controller that will be called when a browser asks for this page
  (here "welcome.Welcome.home").

This is the basic definition of a route.  A route can have more arguments
(but not less).  If you want to add a new route, just add three new
definitions in the routing configuration.  We will do it in the next
chapter of this tutorial.

Let's see what a controller looks like.

Controllers and actions
-----------------------

Return in your bundle's directory ("try-pa" -> "bundles" -> "welcome")
and go to the "controllers" sub-directory.  In this directory are
stored Python file (with the ".py" extension).

**Controllers are classes**.  Each class is stored in a separate file.
The class name is a capitaled version of the file.  Here, for instance,
we have the "welcome.py" file that contains the "Welcome" class.
Open the file with your favorite editor.  Inside, you should find
something like::

    from controller import Controller

    class Welcome(Controller):

        def home(self):
            return self.render("welcome.home")

* The first line is a simple import.  Your controllers will most likely
  have this line somewhere at the top.  The "controller" module is
  defined in Python Aboard.
* The third line (after the blank line) is the class definition and if
  you did some Python before, you shouldn't be surprise.  We create
  the "Welcome" class inherited from "Controller".  If you don't know
  what these terms mean, you can just remember the syntax to create
  a controller (it will always be class, a space, the controller's name
  (with a capital first letter) and then the "(Controller):" part).
* The fifth line (after one more blank line) is a method definition.
  An instance method, as you may see:  the first agument is "self".
  One more time, if you don't understand the code, just remember it.
  "def" is a keyword, then a space, then the method's name, then
  between parentheses the instance "self" and then a new colon.
* The last line of our controller is the only line of our method.  It
  returns what should be sent to the client's browser.  This result is
  generated by the "render" method.

Rendering is good but not that simple.  You can edit the last line
to replace::

    return self.render("welcome.home")

by::

    return "<h1>Welcome Aboard</h1>"

You can launch the server with the "start server" command.  Then go to
`<http://localhost:9000/>`_ and you should see the new page.

So what you should remember:

* Controllers are classes inherited from "Controller"
* Methods (controller's actions) should return what will be sent to
  the user's browser.

You should now be able to understand the last line of our route::

      controller: welcome.Welcome.home

* "welcome" is the bundle.
* "Welcome" (with a capital "W") is the class's name
* "home" is our action, our method name.

So when a user asks the server to see the "/" page, the server calls
the "home" action of the "Welcome" controller in the "welcome" bundle.

Now I will explain what this "render" method does.

Using views to render pages
---------------------

As you saw in the previous section, you can write the HTML code in your
method and return it.  That's possible, but not a good practice for
some reasons.  The most important one is that this is possible and
understandable when you have a tiny web site (like now), but what will
happen when you have more than one page?  And when you have very long
pages?

So let's talk about views:  views are templates, files in which you can
describe your page and do a lot of more complex actions, like browse
all the users to display them in a tables.  The "render" method that was
used in the "home" action can load a template and return it's content::

    return self.render("welcome.home")

The "render" method takes at least one pareameter:  the path leading
to the template file.  It's not a standard path, though, it's a
shortcut using dots for delimiters, like the controller's definition
in the "routing.yml" file.

* The first part is the bundle's name
* The second part is the path inside the "views" sub-directory of the
  bundle.  The file extension is not mentioned because it will always be
  "jj2" (for Jinja2, the templating system used by Python Aboard).

So the render("welcome.home") method will look for a template in the
"bundles/welcome/views/home.jj2" file.  If the path was
"welcome.say.hello", it will look for the file
"bundles/welcome/views/say/hello.jj2".  If you don't understand how it
works, don't worry, it will be more obvious after some practice.

For the time being, you can open the template file.  It's in the
bundle's directory, sub-directory "views" and is called "home.jj2".  Open
it with your favorite editor, one more time (don't worry about the
extension, it's really like a text file)::

    <% extends "layout/base.jj2" %>
    <% block title %>Python Aboard - welcome!<% endblock %>
        <% block content %>
            <h1>Congratulations!</h1>
            <p>You have just reached the welcome page.</p>
        <% endblock %>

Well, it's a little more complicated than expected, right?  But
hopefully not very long.  As you see, templates contain HTML tags
(like "<h1>" or "<p>").  They also contain specific tags
("<% tag_name %>") and that's the difference between a standard HTML
file and a template.  Let's see line by line:

* The first line uses the "extends" tag.  This tag looks for the
  specified template, loads it and applies the current template above
  the extended one.  If you have already written HTML pages, maybe you
  had to write a lot of times the same code ("<html>", "<head>",
  "<title>" and so forth).  The "extend" tag allows us to write the HTML
  code that will remain the same for almost all pages in a seperate
  file and then load it.  It's a little complicated, we will see more
  details afterwards.
* The second line uses the "<% block ... %>" tag.  It's another power
  of templates:  in the parent template (the one extended the line
  just above), there are different block definitions.  These blocks
  are set here, in the child template.  You can think of it as
  suspension points:  in the parent template, you could find something
  like "<title>... insert the title here...</title>" and in the
  child template, you replace the "..." by your page's title.  Blocks
  are used to extend or replace some portions of the page.  Here, the title.
* And beginning at the third line, the content.  It's very similar to
  the second line, except that the block here is on multiple lines.  As
  you see, you enter in this block the content you want to display.

Extend templates is a little hard to understand.  It may help to look
at the HTML code we get when we visit the `/ <http://localhost:9000/>`_
page.

To do it, remember that you have to return the template rendered in your
action.

File "bundles/welcome/controller/welcome.py"::

    from controller import Controller

    class Welcome(Controller):

        def home(self):
            return self.render("welcome.home")

Now launch the server tiwh the "start server" command and visit
`<http://localhost:9000/>`_.  You should obtain the following HTML code::

    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>Python Aboard - welcome!</title>
        <link rel="stylesheet" href="/static/design.css" />
    </head>
    <body>
         <div id="content">
             <h1>Congratulations!</h1>
             <p>You have just reached the welcome page.</p>
         </div>
    </body>
    </html>

In your template file "welcome.home", you just defined the title and
content. Everything else was in the parent template.

*Where is this parent template, exactly?*

The parent template is in the layout directory.  Outside of your bundle, in
other words.  The question why is very interesting.  Why is this parent
template outside of our bundle?  Because it will be used by different
bundles:  if we create a second bundle with different pages, most of
our templates will extend the parent template.  If you want to change
the design of your site, you just have to modify the parent
template... and ALL your pages in different bundles will be affected by it.

Let's make a very simple test to change the content of our home page.

File "bundles/welcome/views/home.jj2"::

    <% extends "layout/base.jj2" %>
    <% block title %>Welcome to my new site<% endblock %>
        <% block content %>
            <h1>I'm building it</h1>
            <p>Just wait a little longer and it will be working just fine!</p>
        <% endblock %>

Save the file and visit the `<http://localhost:9000/>`_ page (with the
server running).  You should see your new page.

The templating system is powerful and has a lot of possibilities.  We
just saw the basis of it and we will see more in the next chapters
of this tutorial.

Bring it together
-----------------

By now you should have a better idea of what happens when a client tries
to access the `/ <http://localhost:9000/>`_ page:

#. Python Aboard look for the right route and find it.  It was
   defined in the "welcome" bundle.
#. It calls the controller connected to the route.  The 'home' method
   (the action) is called.
#. The "home" method returns the rendered template "welcome.home".
   The view in "bundles/welcome/views/home.jj2" is loaded and
   returned to the user's browser.

You will get used to this process.  Sometimes, some new steps will
be added but these three steps will remain in almost any case.