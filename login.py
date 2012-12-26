import webapp2
import utils
from main import BaseHandler
from google.appengine.ext import db

class Login(BaseHandler):
    
    def get(self):
        self.render("login.html")
    
    def post(self):

        username = self.request.get('username')
        pw = self.request.get('password')
        error = ''
        
        data = db.GqlQuery("select * from Users order by user_name")
        for entry in data:
            user_name = entry.user_name
            user_pass = entry.user_pass
            if user_name == username:
                check = utils.valid_pw(username,pw,user_pass)
                if check:
                    user_id = str(entry.key().id())
                    user_pass_string = str(utils.make_pw_hash(username,pw))
                    self.response.headers.add_header('Set-Cookie', 'user_id=%s|%s;Path=/' % (user_id,user_pass_string))
                    self.redirect('/homework')
#                    self.redirect('/blog/welcome')
                else:
                     error = 'Sorry Invalid Login, Please try again.'
            else:
                error = "Username not found."

        self.render('login.html', error = error, username = username)
      
app = webapp2.WSGIApplication([('/',Login)
], debug=True)
#app = webapp2.WSGIApplication([('/blog/login',Login)
#], debug=True)