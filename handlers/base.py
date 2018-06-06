import os
import jinja2
import webapp2
import uuid

from google.appengine.api import users, memcache

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    # TODO: Add generate_csrf_token=Bool flag.
    def render_template(self, view_filename, params=None):
        if not params:
            params = {}

        cookie_law = self.request.cookies.get('cookie_law')

        if cookie_law:
            params['cookies'] = True

        # User logged in or logged out.
        logged_user = users.get_current_user()

        if logged_user:
            params['user'] = logged_user
            # Redirect logged out users to home '/'.
            params['logout_url'] = users.create_logout_url('/')
        else:
            # Redirect logged in users to home '/'.
            params['login_url'] = users.create_login_url('/')

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

    def render_template_with_csrf(self, view_filename, params=None):
        logged_user = users.get_current_user()

        csrf_token = str(uuid.uuid4())

        memcache.add(key=csrf_token, value=logged_user.email(), time=600)

        context = {
            'csrf_token': csrf_token,
        }
        context.update(params or {})

        return self.render_template(view_filename, params=context)
