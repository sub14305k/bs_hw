import webapp2
import utils
from main import BaseHandler
from database import Users
from google.appengine.ext import db

class Register(BaseHandler):
    
    def get(self):

        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                message = 'You are already registered!'
                self.render("welcome.html", user = globals.users, message = message)
        else:
            self.render("register.html")
            
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
            self.render("register.html",error_user = user_error ,error_pass = pass_error,error_verify = verify_error,error_email = email_error,username = user_input,email = email_input)
        else:
            hash_pass = utils.make_pw_hash(user_input,password_input)
            user_input = str(user_input)
            user_taken = False
            email_taken = False
            data = db.GqlQuery("select * from Users order by user_name")
            for entry in data:
                user = entry.user_name
                email= entry.user_email
                if user == user_input:
                    user_taken = True
                if email == email_input and email != '':
                    email_taken = True
            if user_taken or email_taken:
                user_error = 'Sorry, the username you selected is already taken'
                email_error= 'Sorry, this email is already registered'
                if user_taken and email_taken:
                    self.render('register.html', error_user = user_error, error_email = email_error)
                if user_taken:
                    self.render('register.html', error_user = user_error, email = email_input)
                else: 
                    self.render('register.html', error_email = email_error, username = user_input)
            else:
                new = Users(user_name = user_input, user_pass = hash_pass, user_email = email_input)
                new.put()
                            
                self.response.headers.add_header('Set-Cookie', 'user_id=%s|%s; Path=/' % (new.key().id(),hash_pass))
                self.redirect('/homework')

class Welcome(BaseHandler):
       def get(self):

        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                self.render('welcome.html', user = globals.users)
        else:
            self.redirect('/blog/signup')
            
app = webapp2.WSGIApplication([('/blog/signup',Register),
                               ('/blog/welcome', Welcome)
], debug=True)