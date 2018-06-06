from google.appengine.ext import ndb


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
            title=title,
            content=content,
            author_email=author_email,
        )

        new_topic.put()

        return new_topic

    # Delete Topics here if admin or author. Also delete its comments.
    @classmethod
    def delete(cls, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        topic.deleted = True
        topic.put()
        return topic

    # users.is_current_user_admin()
