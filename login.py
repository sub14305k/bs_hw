import webapp2
import utils
from main import BaseHandler
from google.appengine.ext import db
import globals


class Login(BaseHandler):
    
    def get(self):
        current_url = self.request.url.split('/')[-1]
        if current_url == 'login':
            self.render("login.html")
        else:
            self.render("index.html")
    
    def post(self):
        
        globals.init()
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
                    current_url = self.request.url.split('/')[-1]
                    if current_url == 'login':
                        self.redirect('/wiki/')
                    else: 
                        self.redirect('/homework')

                else:
                     error = 'Sorry Invalid Login, Please try again.'
            else:
                error = "Username not found."

        self.render('login.html', error = error, username = username)
      
app = webapp2.WSGIApplication([('/', Login),
                               ('/wiki/login', Login)
#                               ('/homework/login', Login)
], debug=True)