#!/usr/bin/env python
import webapp2

from handlers.home import HomeHandler
from handlers.cookie import CookieAlertHandler
from handlers.topic import TopicAddHandler, TopicDeleteHandler, TopicDetailsHandler
from handlers.comment import CommentAddHandler, CommentListHandler
from workers.email_new_comment import EmailNewCommentWorker
from cron.delete_topics import DeleteTopicsCron

# Routes
app = webapp2.WSGIApplication([
    webapp2.Route('/', HomeHandler, name='home-page'),
    webapp2.Route('/set-cookie', CookieAlertHandler, name='set-cookie'),
    webapp2.Route('/topic/add', TopicAddHandler, name='topic-add'),
    webapp2.Route('/topic/<topic_id:\d+>/delete', TopicDeleteHandler, name='topic-delete'),
    webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetailsHandler, name='topic-details'),
    webapp2.Route('/topic/<topic_id:\d+>/comment/add', CommentAddHandler, name='comment-add'),
    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker, name='task-email-new-comment'),
    webapp2.Route('/my-comments', CommentListHandler, name='comment-list'),
    webapp2.Route('/cron/delete-topics', DeleteTopicsCron, name='cron-delete-topics'),
], debug=True)
