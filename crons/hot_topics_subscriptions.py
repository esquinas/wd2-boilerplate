from datetime import datetime, timedelta

from handlers.base import BaseHandler
from models.topic import Topic

class HotTopicsSubscriptions(BaseHandler):
    one_day_ago = datetime.now() - timedelta(hours=24)

    all_topics = Topic.query(Topic.deleted == False)
    hottest_topics = all_topics.filter(Topic.created < one_day_ago)
    topics_to_email = hottest_topics.fetch()

    for topic in topics_to_email:
        pass

