from model import *

class Group(Model):

    """A group model."""

    name = String()
    users = HasMany("auth.User")
