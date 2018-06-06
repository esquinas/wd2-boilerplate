#!/usr/bin/env python
import webapp2

from handlers.home import HomeHandler
from handlers.cookie import CookieAlertHandler
from handlers.topic import TopicAddHandler, TopicDetailsHandler
from handlers.comment import CommentAddHandler
from workers.email_new_comment import EmailNewCommentWorker

# Routes
app = webapp2.WSGIApplication([
    webapp2.Route('/', HomeHandler, name='home-page'),
    webapp2.Route('/set-cookie', CookieAlertHandler, name='set-cookie'),
    webapp2.Route('/topic/add', TopicAddHandler, name='topic-add'),
    webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetailsHandler, name='topic-details'),
    webapp2.Route('/topic/<topic_id:\d+>/comment/add', CommentAddHandler, name='comment-add'),
    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker, name='task-email-new-comment'),
], debug=True)
