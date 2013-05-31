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
that's why `WordPress' <http://wordpress.com/>`_ is so popular.

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
* temlates: templates are used to describe the dynamic content of a
  page.  Basically, a template could represent some pages on your site.
* controllers: controllers are functions (or methods, to be more exact)
  that will be called for a certain route and bring everhing together.
* services: services are objects dedicated to something very
  specific.  The most obvious service is used to send e-mails, for instance.
* ...

Don't worry if you don't understand the listed functionalities:  we will
see them one at a time.