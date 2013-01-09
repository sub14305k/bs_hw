import webapp2
import json
import utils
from database import Users
 

class BaseHandler(webapp2.RequestHandler):
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return utils.render_str(template, **params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; Charset = UTF-8'
        self.write(json_txt)
        
class index(BaseHandler):
    def get(self):
        self.render("index.html")
        
class Homework(BaseHandler):
    
    def get(self):

        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                self.render("homework.html", user = globals.users)
            else:
                get_user = utils.check_cookie(self)
                globals.users = get_user
                self.render("homework.html", user = globals.users)
        else:
            self.redirect('/')

class Coursework(BaseHandler):
    
    def get(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                self.render("course_work.html", user = globals.users)
        else:
            self.redirect('/')

class HelloUdacity(BaseHandler):
    
    def get(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                self.render("hello.html", user= globals.users)
        else:
            self.redirect('/')
         
app = webapp2.WSGIApplication([('/homework', Homework),
                               ('/course_work', Coursework),
                               ('/unit1/helloudacity', HelloUdacity)
], debug=True)
