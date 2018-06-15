import os
import re
import unittest
import webapp2
import webtest

from google.appengine.ext import testbed
from google.appengine.api import memcache

from handlers.topic import TopicAddHandler, TopicDetailsHandler


VALID_USER_EMAIL = 'some.user@example.com'


class TopicDetailsHandlerTest(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/topic/add', TopicAddHandler, name='topic-add'),
                webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetailsHandler, name='topic-details'),
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()

        os.environ['USER_EMAIL'] = VALID_USER_EMAIL

        # Create one topic
        csrf_token = '00000000-1111-2222-3333-444444444444'
        memcache.add(key=csrf_token, value=VALID_USER_EMAIL, time=600)

        request_args = {
            'title': 'First Topic',
            'text': 'Test text...',
            'author_email': os.environ['USER_EMAIL'],
            'csrf-token': csrf_token,
        }
        response = self.testapp.post('/topic/add', request_args)

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_topic_details_returns_ok_status(self):
        expected = 200 # Ok
        response = self.testapp.get('/topic/1/details')
        self.assertEqual(response.status_int, expected)

    def test_get_topic_details_when_user_not_logged_in(self):
        os.environ['USER_EMAIL'] = ''
        expect_success = 200 # Ok
        expected = r'((log[ -]?in)|(logged in))'

        response = self.testapp.get('/topic/1/details')
        self.assertEqual(response.status_int, expect_success)
        self.assertFalse(re.search(r'Created', response.body, re.IGNORECASE))
        self.assertTrue(re.search(r'Error', response.body, re.IGNORECASE))
        self.assertTrue(re.search(expected, response.body, re.IGNORECASE),
                      'Should not show topic details when user is not logged in.\nBody\n' + response.body)


