import webapp2
from main import BaseHandler
import utils

class WikiPage(BaseHandler):
    def get(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                self.render("wiki_page.html", user = globals.users)
            else:
                get_user = utils.check_cookie(self)
                globals.users = get_user
                self.render("wiki_page.html", user = globals.users)
        else:
            self.redirect('/wiki/signup')

class WikiSignup(BaseHandler):
     
    def get(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                self.redirect('/wiki')
        else:
            self.render("wiki_signup.html")
    
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
            self.render("wiki_signup.html",error_user = user_error ,error_pass = pass_error,error_verify = verify_error,error_email = email_error,username = user_input,email = email_input)
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
                    self.render('wiki_signup.html', error_user = user_error, error_email = email_error)
                if user_taken:
                    self.render('wiki_signup.html', error_user = user_error, email = email_input)
                else: 
                    self.render('wiki_signup.html', error_email = email_error, username = user_input)
            else:
                new = Users(user_name = user_input, user_pass = hash_pass, user_email = email_input)
                new.put()
                            
                self.response.headers.add_header('Set-Cookie', 'user_id=%s|%s; Path=/' % (new.key().id(),hash_pass))
                self.redirect('/wiki')

class WikiLogin(BaseHandler):
     def get(self):
        self.render("wiki_login.html")

class WikiLogout(BaseHandler):
     def get(self):
        self.render("wiki_logout.html")
        
class WikiEdit(BaseHandler):
     def get(self):
        self.render("wiki_edit.html")     

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/wiki/wiki_page/(?:[a-zA-Z0-9_-]+/?)*', WikiPage),
                               ('/wiki/signup', WikiSignup),
                               ('/wiki/login', WikiLogin),
                               ('/wiki/logout', WikiLogout),
                               ('/wiki/_edit', WikiEdit)
], debug=True)