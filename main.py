#!/usr/bin/env python
import webapp2

from handlers.home import HomeHandler
from handlers.cookie import CookieAlertHandler
from handlers.topic import TopicAddHandler, TopicListHandler, TopicDetailsHandler

# Routes
app = webapp2.WSGIApplication([
    webapp2.Route('/', HomeHandler, name='home-page'),
    webapp2.Route('/set-cookie', CookieAlertHandler, name='set-cookie'),
    webapp2.Route('/topic/add', TopicAddHandler, name='topic-add'),
    webapp2.Route('/topic/list', TopicListHandler),
    webapp2.Route('/topic/<topic_id:\d+>', TopicDetailsHandler, name='topic-details'),
], debug=True)
