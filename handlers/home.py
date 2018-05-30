#!/usr/bin/env python
from base import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        return self.render_template("home.html")
