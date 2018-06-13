# -*- coding: utf-8 -*-

from handlers.base import BaseHandler
from google.appengine.api import mail, app_identity


class EmailNewCommentWorker(BaseHandler):
    # TODO: Do not send new comment to comment author.
    def post(self):
        app_id = app_identity.get_application_id()
        hostname = app_identity.get_default_version_hostname()

        topic_author_email = self.request.get('topic-author-email')
        topic_title = self.request.get('topic-title')
        topic_id = self.request.get('topic-id')

        text =  "Hi!\n\n"
        text += "Your topic {} received a new comment!\n\n".format(topic_title)
        text += "To see it click on this link https://{0}/topic/{1}/details\n\n".format(hostname, topic_id)

        html = """<p>Hi!</p>
               <p>Your topic <strong>{0}</strong> received a new comment!</p>

               <p>Click <a href="https://{1}/topic/{2}/details">on this link</a> 
               to see it.</p>
               """.format(topic_title, hostname, topic_id)

        mail.send_mail(
            sender='no-reply@{}.appspotmail.com'.format(app_id),
                       to=topic_author_email,
                       subject='New comment on your topic',
                       body=text,
                       html=html,
        )
