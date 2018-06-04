import uuid

from google.appengine.api import users, memcache

from handlers.base import BaseHandler
from models.topic import Topic


class TopicAddHandler(BaseHandler):
    def get(self):

        csrf_token = str(uuid.uuid4())

        memcache.add(key=csrf_token, value=True, time=600)

        context = {
            "csrf_token": csrf_token
        }

        return self.render_template('topic_add.html', params=context)

    def post(self):
        csrf_token = self.request.get('csrf-token')
        mem_token = memcache.get(key=csrf_token)

        if not mem_token:
            return self.write('This website is protected against CSRF attacks :P')

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


class TopicListHandler(BaseHandler):
    def list(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        context = {
            "topic": topic,
        }
        return self.render_template('topic_list.html', params=context)