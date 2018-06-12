from google.appengine.ext import ndb
from utils.helpers import normalize_email


class TopicSubscription(ndb.Model):
    user_email = ndb.StringProperty()
    topic_id = ndb.IntegerProperty()

    @classmethod
    def create(cls, user, topic):
        user_email = normalize_email(user.email())

        new_topic_subscription = cls(
            user_email=user_email,
            topic_id=topic.key.id(),
        )
        new_topic_subscription.put()

        return new_topic_subscription

    @classmethod
    def is_user_subscribed(cls, user, topic):
        '''Class method to check if user is subscribed to a topic.

        :param user:
        :type User
        :param topic: Topic to check if User is subscribed to it.
        :type   Topic
        :return: Boolean
        '''
        topic_subscriptions = cls.query(cls.topic_id == topic.key.id())
        subscriptions = topic_subscriptions.filter(cls.user_email == user.email())
        subscription_length = subscriptions.count()

        return subscription_length > 0