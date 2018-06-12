from handlers.base import BaseHandler
from google.appengine.api import mail, app_identity


class EmailNewCommentWorker(BaseHandler):
    def post(self):
        hostname = app_identity.get_default_version_hostname()

        topic_author_email = self.request.get('topic-author-email')
        topic_title = self.request.get('topic-title')
        topic_id = self.request.get('topic-id')

        mail.send_mail(
            sender='no-reply@smartninjawd2-ge-projects.appspotmail.com',
                       to=topic_author_email,
                       subject='New comment on your topic',
                       body="""
                           Your topic <strong>{0}</strong> received a new comment!

                           Click <a href="https://{1}/topic/{2}">on this link</a> 
                           to see it.
                           """.format(
                           topic_title,
                           hostname,
                           topic_id,
                       )
        )
