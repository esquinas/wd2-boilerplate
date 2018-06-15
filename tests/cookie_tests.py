import os
import unittest
import webapp2
import webtest

from google.appengine.ext import testbed

from handlers.home import HomeHandler
from handlers.cookie import CookieAlertHandler

VALID_USER_EMAIL = 'some.user@example.com'


class CookieHandlerTest(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/', HomeHandler, name='home-page'),
                webapp2.Route('/set-cookie', CookieAlertHandler, name='set-cookie'),
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()

        os.environ['USER_EMAIL'] = VALID_USER_EMAIL

    def tearDown(self):
        self.testbed.deactivate()

    def test_post_create_cookie_redirects(self):
        expect_redirect = 302 # Redirected after cookie creation
        expected = '/' # Home
        response = self.testapp.post('/set-cookie')

        self.assertEqual(response.status_int, expect_redirect)
        self.assertTrue(response.location.endswith(expected),
                        'Cookie creation should redirect to home page.\nLocation:\n' + response.location)



