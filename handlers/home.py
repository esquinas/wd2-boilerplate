from google.appengine.api import users

from utils.helpers import normalize_email
from handlers.base import BaseHandler
from models.topic import Topic

class HomeHandler(BaseHandler):
    def get(self):
        is_admin = users.is_current_user_admin()

        # topics = Topic.query(Topic.deleted == False).fetch()
        topics = Topic.list().fetch()

        context = {
            'topics': topics,
            'can_make_changes': is_admin,
        }

        return self.render_template('home.html', params=context)
