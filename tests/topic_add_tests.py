import os
import uuid
import unittest
import webapp2
import webtest

from google.appengine.ext import testbed
from google.appengine.api import memcache

from handlers.topic import TopicAddHandler, TopicDetailsHandler

VALID_USER_EMAIL = 'some.user@example.com'
INVALID_USER_EMAIL = 'invalid-email!'

class TopicTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/topic/add', TopicAddHandler, name='topic-add'),
                webapp2.Route('/topic/<topic_id>/details', TopicDetailsHandler, name='topic-details')
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        # self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_topic_add_handler_returns_ok_status(self):
        expected = 200
        response = self.testapp.get('/topic/add')
        self.assertEqual(response.status_int, expected,
                         'GET topic add address (/topic/add) should return an ok status (200).')

    def test_post_topic_add_handler_should_redirect(self):
        # Arrange
        csrf_token = '00000000-1111-2222-3333-444444444444'
        memcache.add(key=csrf_token, value=VALID_USER_EMAIL, time=600)

        request_args = {
            'title': 'Test Title',
            'text': 'Test text...',
            'csrf-token': csrf_token,
        }
        # Act
        response = self.testapp.post('/topic/add', request_args)

        # Assert
        expected = 302 # Redirected
        self.assertEqual(response.status_int, expected,
                         'POST topic add should return a redirected status (302).\nBody:\n' +
                          response.body)



