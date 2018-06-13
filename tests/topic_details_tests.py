import os
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
        request_args = {
            'title': 'First Topic',
            'text': 'Test text...',
            'csrf-token': csrf_token,
        }
        self.testapp.post('/topic/add', request_args)

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_topic_details_returns_ok_status(self):
        expected = 200 # Ok
        response = self.testapp.get('/topic/1/details')
        self.assertEqual(response.status_int, expected)

