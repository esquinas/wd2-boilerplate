from google.appengine.ext import ndb
from utils.helpers import normalize_email


class WebsiteSubscription(ndb.Model):
    user_email = ndb.StringProperty()

    @classmethod
    def create(cls, user):
        user_email = normalize_email(user.email())

        new_website_subscription = cls(
            user_email=user_email,
        )
        new_website_subscription.put()

        return new_website_subscription

    @classmethod
    def list_emails(cls):
        '''Class method to list all subscribers' emails.

        :return: A list of strings containing subscribers' emails.
        :type string[]
        '''
        all_subscriptions = cls.query()
        return [subscriber.user_email for subscriber in all_subscriptions]

    @classmethod
    def is_user_subscribed(cls, user):
        '''Class method to check if user is subscribed to the website.

        :param user:
        :type User
        :return: Boolean
        '''
        subscriptions = cls.query(cls.user_email == user.email())
        subscription_length = subscriptions.count()

        return subscription_length > 0