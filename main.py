import webapp2
import os
import jinja2
import re


from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

class Art(db.Model):
        title = db.StringProperty(required = True)
        art = db.TextProperty(required = True)
        created = db.DateTimeProperty(auto_now_add = True)

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Blog_db(db.Model):
        subject = db.StringProperty(required = True)
        content = db.TextProperty(required = True)
        created = db.DateTimeProperty(auto_now_add = True)

        def render(self):
            self._render_text = self.content.replace('\n', '<br>')
            return render_str("post.html", p = self)

class Index(BaseHandler):
    def get(self):
        self.render("index.html")

class coursework(BaseHandler):
    def get(self):
        self.render("course_work.html")

class HelloUdacity(BaseHandler):
    def get(self):
        self.render("hello.html")

rot_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
rot_list2 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def ROT13(s):
    replaced_string = []
    for char in s:
        if char not in rot_list and char not in rot_list2:
            replaced_string += char
        if char in rot_list:
            index = rot_list.index(char)
            if index < 13:
                replaced_string += rot_list[index + 13]
            if index >= 13:
                replaced_string += rot_list[index - 13]
        if char in rot_list2:
            index = rot_list2.index(char)
            if index < 13:
                replaced_string += rot_list2[index + 13]
            if index >= 13:
                replaced_string += rot_list2[index - 13]
    replaced_string = ''.join(replaced_string)
    return replaced_string

class Rot13(BaseHandler):
    
    def get(self):
        self.render("rot13-form.html")
    def post(self):
        user_input = self.request.get("text")
        if user_input == "":
            self.render("rot13-form.html", error = "You didn't enter any text. Please try again.")
        else:  
          convert = ROT13(user_input)
          self.render("rot13-form.html",user_input = convert)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASS_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BaseHandler):
    
    def get(self):
        self.render("signup.html")
    
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
            self.render("signup.html",error_user = user_error ,error_pass = pass_error,error_verify = verify_error,error_email = email_error,username = user_input,email = email_input)
        else:
          self.redirect('/unit2/welcome?username=' + user_input)

class Welcome(BaseHandler):
       def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/unit2/signup')

class ASCIIChan(BaseHandler):

    def render_ASCII_page(self, title="", art = "", error = ""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        self.render("ASCIIChan.html", title = title, art = art, error = error, arts = arts)

    def get(self):
        self.render_ASCII_page()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if art and title:
            a = Art(title = title, art = art)
            a.put()

            self.redirect("/course_work/unit3/ASCIIChan")
        else:
            error = "We need both title and some artwork!"
            self.render_ASCII_page(title,art,error) 

class Blog_Page(BaseHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Blog_db ORDER BY created DESC LIMIT 10")
        self.render("blog.html", posts = posts)

class Create_Blog(BaseHandler):
    
    def get(self):
        self.render("newpost.html")
    def post(self):
        subject = self.request.get("subject")
        contents = self.request.get("content")

        if subject and contents:
            s = Blog_db(parent = blog_key(), subject = subject, content = contents)
            s.put()

            self.redirect("/blog/%s" % str(s.key().id()))
        else:
            error = "We need both subject and content!"
            self.render("newpost.html", subject = subject, content = contents, error = error)

class Permalink(BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('Blog_db', int(post_id), parent = blog_key())
        post = db.get(key)
        
        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)
         
app = webapp2.WSGIApplication([('/', Index),
                               ('/course_work', coursework),
                               ('/course_work/unit3/ASCIIChan', ASCIIChan),
                               ('/unit1/helloudacity', HelloUdacity),
                               ('/unit2/rot13', Rot13),
                               ('/unit2/signup',Signup),
                               ('/unit2/welcome', Welcome),
                               ('/blog/?', Blog_Page),
                               ('/blog/newpost', Create_Blog),
                               ('/blog/([0-9]+)', Permalink)
], debug=True)
