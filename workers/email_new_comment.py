from handlers.base import BaseHandler
from google.appengine.api import mail


class EmailNewCommentWorker(BaseHandler):
    def post(self):
        topic_author_email = self.request.get('topic-author-email')
        topic_title = self.request.get('topic-title')
        topic_id = self.request.get('topic-id')

        mail.send_mail(
            sender='esquinas.enrique@gmail.com',
                       to=topic_author_email,
                       subject='New comment on your topic',
                       body="""
                           Your topic <strong>{0}</strong> received a new comment!

                           Click <a href="https://smartninjawd2-ge-projects.appspot.com/topic/{1}">on this link</a> 
                           to see it.
                           """.format(topic_title, topic_id)
        )
