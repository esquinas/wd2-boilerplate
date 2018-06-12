from google.appengine.api import app_identity
from datetime import datetime, timedelta

from handlers.base import BaseHandler
from models.topic import Topic
from models.website_subscription import WebsiteSubscription

class SendNewTopicsCron(BaseHandler):
    def get(self):
        # Prepare users
        subscriber = WebsiteSubscription.list().fetch()

        # Prepare topics
        one_day_ago = datetime.now() - timedelta(hours=24)

        hottest_topics = Topic.list().filter(Topic.created > one_day_ago)
        topics_to_email = hottest_topics.fetch()

        # Prepare email
        body_content = []
        hostname = app_identity.get_default_version_hostname()

        topics = []

        for topic in topics_to_email:
            topics.append(topic.key.id())

                '''
                subscriptions = TopicSubscription.query(TopicSubscription.topic_id == topic.key.id()).fetch()

        subscribers = [topic.author_email, ]

        for subscription in subscriptions:
            if subscription.user_email != user_email:
                subscribers.append(subscription.user_email)

        # Send notification to topic author and subscribers.
        for email in subscribers:
            params = {
                'topic-author-email': email,
                'topic-title': topic.title,
                'topic-id': topic.key.id(),
            }
            taskqueue.add(url='/task/email-new-comment', params=params)
                '''