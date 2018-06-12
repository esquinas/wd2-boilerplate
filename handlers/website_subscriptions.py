from google.appengine.api import users

from datetime import datetime, timedelta

from handlers.base import BaseHandler
from models.topic import Topic
from models.website_subscription import WebsiteSubscription

class WebsiteSubscriptionsHandler(BaseHandler):
    def get(self):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write('Please login to be allowed to subscribe.')

        WebsiteSubscription.create(user)

        flash = {
            'flash_message': "You've been subscribed succesfully to hot topics.",
            'flash_class': 'alert-success',
        }

        return self.redirect_to('home-page', **flash)

