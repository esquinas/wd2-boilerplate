import uuid

from google.appengine.api import users, memcache

from handlers.base import BaseHandler
from models.topic import Topic


class TopicAddHandler(BaseHandler):
    def get(self):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to post a topic.")

        csrf_token = str(uuid.uuid4())

        memcache.add(key=csrf_token, value=logged_user.email(), time=600)

        context = {
            "csrf_token": csrf_token
        }

        return self.render_template('topic_add.html', params=context)

    def post(self):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write('Please login to be allowed to post a new topic.')

        csrf_token = self.request.get('csrf-token')
        mem_token = memcache.get(key=csrf_token)

        if not mem_token or mem_token != logged_user.email():
            return self.write('This website is protected against CSRF attacks :P')

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

        flash = {
            'flash_message': 'Topic added successfully',
            'flash_class': 'alert-success',
        }

        #return self.redirect_to('topic-details', topic_id=new_topic.key.id())
        return self.redirect_to('topic-details', topic_id=new_topic.key.id(), **flash)


class TopicListHandler(BaseHandler):
    def list(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        context = {
            'topic': topic,
        }

        return self.render_template('topic_list.html', params=context)


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        context = {
            'topic': topic,
            'flash_message': self.request.get('flash_message'),
            'flash_class': self.request.get('flash_class'),
        }

        return self.render_template('topic_details.html', params=context)