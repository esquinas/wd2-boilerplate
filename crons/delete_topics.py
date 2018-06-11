from datetime import datetime

from handlers.base import BaseHandler
from models.topic import Topic

class DeleteTopicsCron(BaseHandler):
    def get(self):
        one_month_ago = datetime.now() - datetime.timedelta(days=30)

        deleted_topics = Topic.query(Topic.deleted == True)
        overdue_topics = deleted_topics.filter(Topic.updated < one_month_ago)
        topics_to_remove = overdue_topics.fetch()

        for topic in topics_to_remove:
            topic.key.delete()
