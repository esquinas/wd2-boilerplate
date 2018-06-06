from google.appengine.api import users, memcache

from utils.decorators import validate_csrf
from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment


class CommentAddHandler(BaseHandler):

    @validate_csrf
    def post(self, topic_id):
        if not topic_id:
            return self.write('Error trying to write a comment into undefined topic!')

        topic = Topic.get_by_id(int(topic_id))

        logged_user = users.get_current_user()

        if not logged_user:
            return self.write('Please login to be allowed to post a new comment.')

        content = self.request.get('comment')


        if (not content) or (not content.strip()):
            return self.write('Empty comments are not allowed!')

        new_comment = Comment.create(
            content=content,
            user=logged_user,
            topic=topic,
        )

        flash = {
            'flash_message': 'Comment added successfully',
            'flash_class': 'alert-success',
        }

        return self.redirect_to('topic-details', topic_id=topic_id, **flash)








