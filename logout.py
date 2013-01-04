import webapp2
from main import BaseHandler

class Logout(BaseHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=;Path=/')
        self.response.headers.add_header('Set-Cookie', 'visits=;Path=/')
        import globals
        globals.users = None
        self.redirect('/')
#        self.redirect('/blog/signup')

#app = webapp2.WSGIApplication([('/blog/logout', Logout)
#], debug=True)
app = webapp2.WSGIApplication([('/unit4/logout',Logout)
], debug=True)