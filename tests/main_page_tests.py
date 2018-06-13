import os
import unittest
import webapp2
import webtest

from google.appengine.ext import testbed
from handlers.home import HomeHandler


class HomePageTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/', HomeHandler, name="home-page"),
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        # self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        # self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_home_page_root_returns_ok_status_when_GET_requested(self):
        get = self.testapp.get('/')  # get home handler
        self.assertEqual(get.status_int, 200,
                         'GET root address (/) should return an ok status (200).')

    def test_home_page_body_includes_website_name(self):
        response = self.testapp.get('/')
        self.assertIn('Ninja Tech Forum', response.body,
                         'Home page should include "Welcome to Ninja Tech Forum".')


