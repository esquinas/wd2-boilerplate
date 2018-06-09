from google.appengine.ext import ndb
from models.comment import Comment
from utils.helpers import normalize_email, escape_html

class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, title, content, author_email):
        new_topic = cls(
            title=escape_html(title),
            content=escape_html(content),
            author_email=normalize_email(author_email),
        )

        new_topic.put()

        return new_topic

    # Delete Topics here if admin or author. Also delete its comments.
    @classmethod
    def delete(cls, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        topic.deleted = True
        topic.put()
        topic.__delete_all_comments()
        return topic

    # Private methods.
    def __delete_all_comments(self):
        all_comments = Comment.query(Comment.deleted == False)
        topic_comments = all_comments.filter(Comment.topic_id == self.key.id())

        for comment in topic_comments:
            Comment.delete(comment.key.id())
