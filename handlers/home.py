from handlers.base import BaseHandler
from models.topic import Topic

class HomeHandler(BaseHandler):
    def get(self):
        topics = Topic.query(Topic.deleted == False).fetch()

        context = {
            'topics': topics,
        }

        return self.render_template('home.html', params=context)
