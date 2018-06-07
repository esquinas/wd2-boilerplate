from google.appengine.api import users, memcache


def validate_csrf(handler):

    def wrapper(self, *args, **kwargs):
        logged_user = users.get_current_user()

        csrf_token = self.request.get('csrf-token')
        mem_token = memcache.get(key=csrf_token)

        if not mem_token or mem_token != logged_user.email():
            return self.write('This website is protected against CSRF attacks :P')
        else:
            return handler(self, *args, **kwargs)

    return wrapper
