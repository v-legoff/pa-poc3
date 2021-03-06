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


"""This module contains a generic class for testing query managers.

You can actually test your data connector without testing the 'querying'
part.  This is a good start for development but of course, in the end,
a data connector should implement ALL possibilities of the query
manager.  These possibilities are tested in this file.

So if you want to test you data connector and query manager, simply
inherit your class from AbstractQMTest as well as from AbstractDCTest.

"""

from datetime import datetime

from model.functions import *
from tests.model import *

class AbstractQMTest:

    """Abstract class for testing query managers.

    This class is abstract.  It shouldn't be considered a regular
    test case and doesn't have enough informations to perform a test.
    It's a base test for a data connector (each data connector should
    have a class inherited from it as well as from DCTest).  This allows
    to test different data connectors to check that each one has the same
    abilities as any other one.

    Testing methods (some could be added, NOT MODIFIED):
        test_op_equal -- test the equal (=) operator

    """

    def create_posts(self):
        """Create three posts with different published_at dates."""
        repository = Post._repository
        post_1 = repository.create(title="post1", content="not yet",
                published_at=datetime.strptime("2000-02-15", "%Y-%m-%d"))
        post_2 = repository.create(title="post2", content="still not",
                published_at=datetime.strptime("2005-12-24", "%Y-%m-%d"))
        post_3 = repository.create(title="post3", content="ahem",
                published_at=datetime.strptime("2013-05-01", "%Y-%m-%d"))
        return (post_1, post_2, post_3)

    def test_op_equal(self):
        """Test that the query manager correctly interpret the = operator."""
        repository = User._repository
        user = repository.create(username="Kredh", password="fore123")
        query = repository.query()
        query.filter("username = ?", "Kredh")
        result = query.execute(many=False)
        self.assertEqual(user.username, result.username)
        self.assertIs(result, user)

    def test_op_notequal(self):
        """Test that the query manager correctly interpret the != operator."""
        repository = User._repository
        kyra = repository.create(username="Kyra", password="just guess")
        carla = repository.create(username="Carla", password="***")
        query = repository.query()
        query.filter("username != ?", "Carla")
        results = query.execute()
        self.assertIn(kyra, results)
        self.assertNotIn(carla, results)

    def test_op_lowerthan(self):
        """Test that the query manager correctly interpret the < operator."""
        repository = Post._repository
        post_1, post_2, post_3 = self.create_posts()
        query = repository.query()
        query.filter("published_at < ?", datetime.strptime("2008", "%Y"))
        results = query.execute()
        self.assertIn(post_1, results)
        self.assertIn(post_2, results)
        self.assertNotIn(post_3, results)

    def test_op_lowerequal(self):
        """Test that the query manager correctly interpret the <= operator."""
        repository = Post._repository
        post_1, post_2, post_3 = self.create_posts()
        query = repository.query()
        query.filter("published_at <= ?",
                datetime.strptime("2005-12-24", "%Y-%m-%d"))
        results = query.execute()
        self.assertIn(post_1, results)
        self.assertIn(post_2, results)
        self.assertNotIn(post_3, results)

    def test_connector_and(self):
        """Test that the 'and' connector works for the query manager."""
        repository = User._repository
        user = repository.create(username="Other", password="asis")
        query = repository.query()
        query.filter("username = ?", "Other")
        query.filter("password = ?", "asis")
        result = query.execute(many=False)
        self.assertIs(result, user)
