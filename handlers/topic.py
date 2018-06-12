from google.appengine.api import users, memcache

from utils.decorators import validate_csrf
from utils.helpers import normalize_email
from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment


class TopicAddHandler(BaseHandler):

    def get(self):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write("Please login before you're allowed to post a topic.")

        return self.render_template_with_csrf('topic_add.html')

    @validate_csrf
    def post(self):
        logged_user = users.get_current_user()

        if not logged_user:
            return self.write('Please login to be allowed to post a new Topic.')

        title_value = self.request.get('title')
        text_value = self.request.get('text')
        author_email = logged_user.email()

        if (not title_value) or (not title_value.strip()):
            return self.write('Title field is required!')

        if (not text_value) or (not text_value.strip()):
            return self.write('Text field is required!')

        new_topic = Topic.create(
            title=title_value,
            content=text_value,
            author_email=author_email,
        )

        flash = {
            'flash_message': 'Topic added successfully',
            'flash_class': 'alert-success',
        }

        return self.redirect_to('topic-details', topic_id=new_topic.key.id(), **flash)


class TopicDeleteHandler(BaseHandler):

    def post(self, topic_id):
        logged_user = users.get_current_user()
        topic = Topic.get_by_id(int(topic_id))

        is_same_author = (topic.author_email == normalize_email(logged_user.email()))
        is_admin = users.is_current_user_admin()

        if is_same_author or is_admin:
            Topic.delete(topic_id)
        else:
            return self.write("Sorry, you're not allowed to delete this topic.")

        return self.redirect_to('home-page')


class TopicDetailsHandler(BaseHandler):

    def get(self, topic_id):
        is_authorized = False
        is_admin = users.is_current_user_admin()

        int_topic_id = int(topic_id)
        topic = Topic.get_by_id(int_topic_id)

        logged_user = users.get_current_user()
        is_same_author = topic.author_email == normalize_email(logged_user.email())

        if is_same_author or is_admin:
            is_authorized = True

        #all_comments = Comment.query(Comment.deleted == False)
        #asorted_topic_comments = all_comments.filter(Comment.topic_id == int_topic_id)
        #comments = asorted_topic_comments.order(Comment.created).fetch()
        query = Comment.filter_by_topic(topic)
        comments = query.order(Comment.created).fetch()

        context = {
            'topic': topic,
            'comments': comments,
            'can_make_changes': is_authorized,
            'flash_message': self.request.get('flash_message'),
            'flash_class': self.request.get('flash_class'),
        }

        return self.render_template_with_csrf('topic_details.html', params=context)
