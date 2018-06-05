import uuid

from google.appengine.api import users, memcache

from handlers.base import BaseHandler
from models.topic import Topic


class CommentAddHandler(BaseHandler):
    def get(self, topic_id):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to add a comment.")

        csrf_token = str(uuid.uuid4())

        memcache.add(key=csrf_token, value=logged_user.email(), time=600)

        context = {
            'csrf_token': csrf_token,
            'topic_id': topic_id,
        }

        return self.render_template('new_comment.html', params=context)


class CommentListHandler(BaseHandler):
    def list(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        context = {
            'topic': topic,
        }

        return self.render_template('topic_comments.html', params=context)




