import webapp2
from main import BaseHandler

class Logout(BaseHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=;Path=/')
        self.response.headers.add_header('Set-Cookie', 'visits=;Path=/')
        self.redirect('/')

app = webapp2.WSGIApplication([('/unit4/logout',Logout)
], debug=True)