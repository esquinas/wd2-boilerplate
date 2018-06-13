# -*- coding: utf-8 -*-

from handlers.base import BaseHandler
from google.appengine.api import mail, app_identity


class EmailNewTopicsWorker(BaseHandler):
    def post(self):
        hostname = app_identity.get_default_version_hostname()

        subscriber_email = self.request.get('subscriber-email')
        body_content = self.request.get('body-content')
        html_content = self.request.get('html-content')

        mail.send_mail(
            sender='no-reply@smartninjawd2-ge-projects.appspotmail.com',
                       to=subscriber_email,
                       subject='New topics',
                       body=body_content,
                       html=html_content,
        )
