from google.appengine.api import app_identity, taskqueue

from datetime import datetime, timedelta

from handlers.base import BaseHandler
from models.topic import Topic
from models.website_subscription import WebsiteSubscription


class SendNewTopicsCron(BaseHandler):
    def get(self):
        subscribers_emails = WebsiteSubscription.list_emails()

        topics_to_email = self.__prepare_new_topics()

        content = self.__prepare_content(topics_to_email)

        for email in subscribers_emails:
            params = {
                'subscriber-email': email,
                'body-content': content,
            }

            taskqueue.add(url='/task/email-new-topics', params=params)

        return None

    # Private methods
    def __prepare_new_topics(self):
        one_day_ago = datetime.now() - timedelta(hours=24)
        hottest_topics = Topic.list().filter(Topic.created > one_day_ago)
        return hottest_topics.fetch()

    def __prepare_content(self, topics):
        hostname = app_identity.get_default_version_hostname()

        topics_ul = '''
            <ul>
                {}
            </ul>
        '''.format(self.__prepare_topics_li(topics))

        # TODO: Handle un-subscriptions by simple link (get).
        unsubscribe_footer = '<a href="#">No automatic unsubscribe link yet, sorry</a>.\n'

        # TODO: Use some kind of template system for different emails.
        content = """
            Hello!
            
            Here you have all topics from yesterday:
            
            {0}
            
            Thanks for your subscription and we hope you liked the read!
            
            Sincerely,
            {1} webmaster
            
            <blockquote>{2}</blockquote>
        """.format(topics_ul, hostname, unsubscribe_footer)

        return content

    def __prepare_topics_li(self, topics):
        li = ''
        hostname = app_identity.get_default_version_hostname()

        for topic in topics:
            li += """
              <li><a href="https://{0}/topic/{1}">{2}</a></li>
              """.format(hostname, topic.key.id(), topic.title)

        return li
