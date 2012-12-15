import webapp2
from main import BaseHandler
from database import Users
from google.appengine.ext import db
import random
import string
import hashlib
from google.appengine.ext.db import SelfReference

def make_salt():
    make_characters = string.letters
    return ''.join(random.sample(make_characters,5))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h,salt)

def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)

class Login(BaseHandler):
    
    def get(self):
        self.render("login.html")
    
    def post(self):
        username = self.request.get('username')
        pw = self.request.get('password')
        error = ''
        has_error = False
        
        data = db.GqlQuery("select * from Users order by user_name")
        for entry in data:
            user_name = entry.user_name
            user_pass = entry.user_pass
            if user_name == username:
                check = valid_pw(username,pw,user_pass)
                if check:
                    user_id = str(entry.key().id())
                    user_pass_string = str(make_pw_hash(username,pw))
                    self.response.headers.add_header('Set-Cookie', 'user_id=%s|%s;Path=/' % (user_id,user_pass_string))
                    self.redirect('/unit4/welcome')
                else:
                     error = 'Sorry Invalid Login, Please try again.'
                     has_error = True
            else:
                error = "Username not found."
                has_error = True
#        if not has_error:
#            html = '''<a href="/unit4/register" id="register_link">signup</a>'''
#            error = "Username not found. Click here to %s" % html
        self.render('login.html', error = error, username = username)
#        
        

app = webapp2.WSGIApplication([('/',Login)
], debug=True)