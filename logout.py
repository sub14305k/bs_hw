import webapp2
from main import BaseHandler

class Logout(BaseHandler):
    
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=;Path=/')
        self.response.headers.add_header('Set-Cookie', 'visits=;Path=/')
        import globals
        globals.users = None
        self.redirect('/')
        
app = webapp2.WSGIApplication([('/wiki/logout',Logout)
], debug=True)