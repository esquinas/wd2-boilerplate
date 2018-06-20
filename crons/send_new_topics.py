# -*- coding: utf-8 -*-

from google.appengine.api import app_identity, taskqueue

from datetime import datetime, timedelta

from handlers.base import BaseHandler
from models.topic import Topic
from models.website_subscription import WebsiteSubscription


class SendNewTopicsCron(BaseHandler):
    def get(self):
        subscribers_emails = WebsiteSubscription.list_emails()

        topics_to_email = self.__prepare_new_topics()

        if len(topics_to_email) == 0:
            return None

        text_content, html_content = self.__prepare_content(topics_to_email)

        # # Uncomment for debugging.
        # print(text_content)
        # print(html_content)

        for email in subscribers_emails:
            params = {
                'subscriber-email': email,
                'body-content': text_content,
                'html-content': html_content,
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
        unsubscribe_link = 'No automatic unsubscribe link yet, sorry'
        unsubscribe_footer = '<a href="#">' + unsubscribe_link + '</a>.\n'

        # TODO: Use some kind of template system for different emails.
        text_content = "Hello!\n\n"
        text_content += "Here you have all topics from yesterday:\n\n"
        text_content += self.__prepare_topics_text(topics)
        text_content += "Thanks for your subscription and we hope you liked the read!\n\n"
        text_content += "Sincerely,\n"
        text_content += "{} webmaster\n\n".format(hostname)
        text_content += "{}".format(unsubscribe_link)

        html_content = """
                       <p>Hello!</p>
                        
                       <p>Here you have all topics from yesterday:</p>
                        
                       {0}
                        
                       <p>Thanks for your subscription and we hope you liked the read!</p>
                        
                       <p>Sincerely,<br>
                       <a href="https://{1}">{1}</a> webmaster.</p>
                        
                       <blockquote>{2}</blockquote>
        """.format(topics_ul, hostname, unsubscribe_footer)

        return text_content, html_content

    def __prepare_topics_li(self, topics):
        li = ''
        hostname = app_identity.get_default_version_hostname()

        for topic in topics:
            li += """
              <li><a href="https://{0}/topic/{1}">{2}</a></li>
              """.format(hostname, topic.key.id(), topic.title)

        return li

    def __prepare_topics_text(self, topics):
        line = ''
        hostname = app_identity.get_default_version_hostname()

        for topic in topics:
            line += "\t- {0}:\n\t  https://{1}/topic/{2}/details\n\n".format(topic.title, hostname, topic.key.id())

        return line

