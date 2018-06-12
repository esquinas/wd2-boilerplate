from google.appengine.api import users, memcache

from utils.decorators import validate_csrf
from utils.helpers import normalize_email
from handlers.base import BaseHandler
from models.topic import Topic
from models.topic_subscription import TopicSubscription


class TopicSubscribeHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))

        context = {
            'topic': topic,
        }

        return self.render_template_with_csrf('topic_subscribe.html', params=context)

    @validate_csrf
    def post(self, topic_id):
        logged_user = users.get_current_user()
        user_email = normalize_email(logged_user.email())

        if not logged_user:
            return self.write("Please login before you're allowed to subscribe to one topic.")

        topic = Topic.get_by_id(int(topic_id))

        is_subscribed = topic.author_email == user_email

        if not is_subscribed:
            # check if user asked to be subscribed
            is_subscribed = TopicSubscription.is_user_subscribed(logged_user, topic)

        if is_subscribed:
            return self.write("You are already subscribed")

        TopicSubscription.create(logged_user, topic)

        return self.redirect_to("topic-details", topic_id=topic.key.id())