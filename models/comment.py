from google.appengine.ext import ndb
from google.appengine.api import taskqueue

from models.topic_subscription import TopicSubscription
from utils.helpers import escape_html, normalize_email


class Comment(ndb.Model):
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    topic_id = ndb.IntegerProperty()
    topic_title = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, content, user, topic):
        """Class method to create new comment.

        :param content: Content text
        :type content: str
        :param user: Author user
        :type user: User
        :param topic: Topic where the comment belongs to
        :type topic: Topic
        :return: New comment
        """
        user_email = normalize_email(user.email())

        new_comment = cls(
            content=escape_html(content),
            topic_id=topic.key.id(),
            topic_title=topic.title,
            author_email=user_email,
        )
        new_comment.put()

        subscriptions = TopicSubscription.query(TopicSubscription.topic_id == topic.key.id()).fetch()

        subscribers = [topic.author_email, ]

        for subscription in subscriptions:
            if subscription.user_email != user_email:
                subscribers.append(subscription.user_email)

        # Send notification to topic author and subscribers.
        for email in subscribers:
            params = {
                'topic-author-email': email,
                'topic-title': topic.title,
                'topic-id': topic.key.id(),
            }
            taskqueue.add(url='/task/email-new-comment', params=params)

        return new_comment

    @classmethod
    def delete(cls, comment_id):
        comment = Comment.get_by_id(int(comment_id))
        comment.deleted = True
        comment.put()
        return comment

    @classmethod
    def filter_by_topic(cls, topic):
        '''Classmethod to filter comments by topic

        :param topic: Topic instance
        :return: Query
        '''
        query = cls.query(cls.deleted == False).filter(cls.topic_id == topic.key.id())
        return query

    @classmethod
    def filter_by_author_email(cls, email):
        '''Classmethod to filter comments by author's email.

        :param email: string
        :return: Query
        '''
        query = cls.query(cls.deleted == False).filter(cls.author_email == email)
        return query


