import uuid

from google.appengine.api import users, memcache

from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment


class CommentAddHandler(BaseHandler):

    def post(self, topic_id):
        if not topic_id:
            return self.write('Error trying to write a comment into undefined topic!')

        topic = Topic.get_by_id(int(topic_id))

        logged_user = users.get_current_user()

        if not logged_user:
            return self.write('Please login to be allowed to post a new comment.')

        csrf_token = self.request.get('csrf-token')
        mem_token = memcache.get(key=csrf_token)

        if not mem_token or mem_token != logged_user.email():
            return self.write('This website is protected against CSRF attacks :P')

        content = self.request.get('comment')
        topic_title = topic.title
        author_email = logged_user.email()

        if (not content) or (not content.strip()):
            return self.write('Empty comments are not allowed!')

        new_comment = Comment(
            content=content,
            topic_id=int(topic_id),
            topic_title=topic_title,
            author_email=author_email,
        )

        new_comment.put()

        flash = {
            'flash_message': 'Comment added successfully',
            'flash_class': 'alert-success',
        }

        return self.redirect_to('topic-details', topic_id=topic_id, **flash)







