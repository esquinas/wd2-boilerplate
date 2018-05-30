from google.appengine.api import users

from handlers.base import BaseHandler
from models.topic import Topic


class TopicAddHandler(BaseHandler):
    def get(self):
        return self.render_template('topic_add.html')

    def post(self):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write('Please login to be allowed to post a new topic.')

        title_value = self.request.get('title')
        text_value = self.request.get('text')
        author_email = logged_user.email()

        if (not title_value) or (not title_value.strip()):
            return self.write('Title field is required!')

        if (not text_value) or (not text_value.strip()):
            return self.write('Text field is required!')

        new_topic = Topic(
            title=title_value,
            content=text_value,
            author_email=author_email,
        )

        new_topic.put()

        return self.write("Topic added successfully. :)")