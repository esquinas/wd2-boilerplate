#!/usr/bin/env python
import webapp2

from handlers.home import HomeHandler
from handlers.cookie import CookieAlertHandler
from handlers.topic import TopicAddHandler, TopicDeleteHandler, TopicDetailsHandler
from handlers.topic_subcription import TopicSubscribeHandler
from handlers.comment import CommentAddHandler, CommentListHandler
from handlers.website_subscriptions import WebsiteSubscriptionsHandler

from workers.email_new_comment import EmailNewCommentWorker
from workers.email_new_topics import EmailNewTopicsWorker

from crons.delete_topics import DeleteTopicsCron
from crons.send_new_topics import SendNewTopicsCron

# Routes
app = webapp2.WSGIApplication([
    webapp2.Route('/', HomeHandler, name='home-page'),
    webapp2.Route('/set-cookie', CookieAlertHandler, name='set-cookie'),
    webapp2.Route('/website-subscription', WebsiteSubscriptionsHandler, name='website-subscription'),
    webapp2.Route('/my-comments', CommentListHandler, name='comment-list'),

    webapp2.Route('/topic/add', TopicAddHandler, name='topic-add'),
    webapp2.Route('/topic/<topic_id:\d+>/delete', TopicDeleteHandler, name='topic-delete'),
    webapp2.Route('/topic/<topic_id:\d+>/details', TopicDetailsHandler, name='topic-details'),
    webapp2.Route('/topic/<topic_id:\d+>/subscribe', TopicSubscribeHandler, name="topic-subscribe"),
    webapp2.Route('/topic/<topic_id:\d+>/comment/add', CommentAddHandler, name='comment-add'),

    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker, name='task-email-new-comment'),
    webapp2.Route('/task/email-new-topics', EmailNewTopicsWorker, name='task-email-new-topics'),

    webapp2.Route('/cron/delete-topics', DeleteTopicsCron, name='cron-delete-topics'),
    webapp2.Route('/cron/send-new-topics', SendNewTopicsCron, name='cron-send-new-topics'),
], debug=True)
