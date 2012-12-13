import webapp2
import re
from main import BaseHandler

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASS_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Register(BaseHandler):
    
    def get(self):
        user_cookie = self.request.cookies.get("user_name")
        if user_cookie:
            self.render("welcome.html", username = user_cookie)
        else:
            self.render("register.html")
    def post(self):
        has_error = False
        user_input = self.request.get('username')
        password_input = self.request.get('password')
        verify_input = self.request.get('verify')
        email_input = self.request.get('email')
        valid_u = valid_username(user_input)
        valid_p = valid_password(password_input)
        valid_e = valid_email(email_input)
        user_error =  ''
        pass_error =  ''
        email_error = ''
        verify_error = ''

        if not valid_u:
             user_error = 'Invalid username, please try again.'
             has_error = True     
        if not valid_p:
             pass_error =  'Invalid password, please try again.'
             has_error = True
        if password_input != verify_input:
            verify_error = 'Passwords do not match, try again.'
            has_error = True
        if not valid_e and email_input != '':
            email_error = 'Invalid email, please try again.'
            has_error = True
        if has_error != False:
            self.render("register.html",error_user = user_error ,error_pass = pass_error,error_verify = verify_error,error_email = email_error,username = user_input,email = email_input)
        else:

          user_input = str(user_input)
          self.render('welcome.html', username = user_input)
          self.response.headers.add_header('Set-Cookie', 'user_name=%s' % user_input)

class Welcome(BaseHandler):
       def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/unit4/register')

app = webapp2.WSGIApplication([('/unit4/register',Register),
                               ('/unit4/welcome', Welcome)
], debug=True)