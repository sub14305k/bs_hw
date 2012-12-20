import webapp2
from main import BaseHandler
import utils

class Signup(BaseHandler):
    
    def get(self):
        self.render("signup.html")
    
    def post(self):
        has_error = False
        user_input = self.request.get('username')
        password_input = self.request.get('password')
        verify_input = self.request.get('verify')
        email_input = self.request.get('email')
        valid_u = utils.valid_username(user_input)
        valid_p = utils.valid_password(password_input)
        valid_e = utils.valid_email(email_input)
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
            self.render("signup.html",error_user = user_error ,error_pass = pass_error,error_verify = verify_error,error_email = email_error,username = user_input,email = email_input)
        else:
          self.redirect('/unit2/welcome?username=' + user_input)

class Welcome(BaseHandler):
       def get(self):
        username = self.request.get('username')
        if utils.valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/unit2/signup')

app = webapp2.WSGIApplication([('/homework/unit2/signup',Signup),
                               ('/unit2/welcome', Welcome)
], debug=True)