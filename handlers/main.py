#!/usr/bin/env python
from base import BaseHandler


class MainHandler(BaseHandler):

    def get(self):
        return self.render_template("main.html")
