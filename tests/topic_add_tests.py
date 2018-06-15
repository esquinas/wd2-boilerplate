import os
import re
import unittest
import webapp2
import webtest

from google.appengine.ext import testbed
from google.appengine.api import memcache

from handlers.topic import TopicAddHandler, TopicDetailsHandler
from models.topic import Topic

VALID_USER_EMAIL = 'some.user@example.com'


class TopicAddHandlerTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/topic/add', TopicAddHandler, name='topic-add'),
                webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetailsHandler, name='topic-details'),
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
        os.environ['USER_EMAIL'] = VALID_USER_EMAIL
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_topic_add_handler_returns_ok_status(self):
        expected = 200
        response = self.testapp.get('/topic/add')
        self.assertEqual(response.status_int, expected,
                         'GET topic add address (/topic/add) should return an ok status (200).')

    def test_get_topic_add_handler_user_not_logged_in(self):
        # Arrange
        os.environ['USER_EMAIL'] = ''

        # Act
        response = self.testapp.get('/topic/add')

        # Assert
        self.assertEqual(response.status_int, 200)
        self.assertIn('Error', response.body)
        self.assertIn('Please login', response.body,
                      'Logged out user should not be able to see topics.' + response.body)

    def test_post_topic_add_handler_user_not_logged_in(self):
        # Arrange
        os.environ['USER_EMAIL'] = ''
        csrf_token = '00000000-1111-2222-3333-444444444444'
        request_args = {
            'title': 'Test Title',
            'text': 'Test text...',
            'csrf-token': csrf_token,
        }
        # Act
        response = self.testapp.post('/topic/add', request_args)
        # Assert
        self.assertEqual(response.status_int, 200)
        self.assertIn('Error', response.body,
                      'Logged out user should not be able to post topics.\nBody:\n' + response.body)

    def test_post_topic_add_handler_should_redirect(self):
        # Arrange
        csrf_token = '00000000-1111-2222-3333-444444444444'
        memcache.add(key=csrf_token, value=VALID_USER_EMAIL, time=600)

        request_args = {
            'title': 'Test Title',
            'text': 'Test text...',
            'author_email': os.environ['USER_EMAIL'],
            'csrf-token': csrf_token,
        }
        # Act
        response = self.testapp.post('/topic/add', request_args)

        # Assert
        expected = 302 # Redirected
        expected_location = r'topic/\d+/details'
        topic = Topic.query().get()

        self.assertEqual(response.status_int, expected,
                         'POST topic add should return a redirected status (302).\nBody:\n' +
                          response.body)
        self.assertTrue(re.search(expected_location, response.location),
                        'Adding a topic should redirect to topic/d+/details.\nLocation:\n' + response.location)
        self.assertEqual(topic.title, request_args['title'])
        self.assertEqual(topic.content, request_args['text'])
        self.assertEqual(topic.author_email, request_args['author_email'])

