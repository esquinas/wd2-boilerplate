#!/usr/bin/env python
from handlers.base import BaseHandler


class CookieAlertHandler(BaseHandler):

    def post(self):
        self.response.set_cookie(key="cookie_law", value="accepted")
        return self.redirect_to("home-page")
