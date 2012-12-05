import webapp2
import re
import io
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

#main = """
<h1>Sign Up</h1>
<br>
<div style="float:left" name="form_container">
    <form method="post">
        <label>Username:
            <input style="margin-left: 50px" type="text" name="username" value="%(username)s" /><span style=" margin-left:15px; color:red" name="error_user">%(error_user)s</span>
        </label>
        <br>
        <br>
        <label>Password:
            <input style="margin-left: 52px" type="password" name="password" value=""><span style=" margin-left:15px; color:red" name="error_pass">%(error_pass)s</span>
        </label>
        <br>
        <br>
        <label>Verify Password:
            <input style="margin-left: 8px" type="password" name="verify" value=""><span style=" margin-left:15px; color:red" name="error_verify">%(error_verify)s</span>
        </label>
         <br>
        <br>
        <label>Email (optional):
            <input style="margin-left: 8px" type="text" name="email" value="%(email)s"><span style=" margin-left:15px; color:red" name="error_email">%(error_email)s</span>
        </label>
        <br>
        <br>
        <input style="margin-left: 75px" type="submit">
     
    </form>
</div>
  
#"""
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASS_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class SignUpHandler(BaseHandler):
    def write_form(self, error_user="", error_pass="", error_verify="",error_email="",username="",password="",verify="",email=""):
        self.response.out.write(main % {'error_user': error_user,'error_pass': error_pass,'error_verify':error_verify,'error_email': error_email,
                                        'username': username,'password': password,'verify' : verify,'email': email})
    def get(self):
        self.write_form()
    def post(self):
        has_error = False
        user = self.request.get('username')
        passwrd = self.request.get('password')
        verify = self.request.get('verify')
        email_input = self.request.get('email')
        valid_u = valid_username(user)
        valid_p = valid_password(passwrd)
        valid_e = valid_email(email_input)
        errorUser =  ''
        errorPass =  ''
        errorEmail = ''
        errorVerify = ''

        if not valid_u:
             errorUser = 'Invalid username, please try again.'
             has_error = True     
        if not valid_p:
             errorPass =  'Invalid password, please try again.'
             has_error = True
        if password != verify:
            errorVerify = 'Passwords do not match, try again.'
            has_error = True
        if not valid_e and email != '':
            errorEmail = 'Invalid email, please try again.'
            has_error = True
        if has_error != False:
            self.render(errorUser = error_user,errorPass = error_pass,errorVerify = error_verify,errorEmail = error_email,user = username,email_input = email)
        else:
          self.redirect('/welcome',username = user_input)

        

class Welcome(BaseHandler):
    def get(self):
         username = self.request.get('username')
         if valid_username(username):
            self.response.out.write('Welcome, ' + username)
         else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),('/welcome', Welcome),('/signup',SignUpHandler)
], debug=True)