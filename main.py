import webapp2
import utils
from database import Users

class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return utils.render_str(template, **params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
class Homework(BaseHandler):
    def get(self):
        user_cookie = self.request.cookies.get('user_id')
        if user_cookie and user_cookie != '':
            user_id = int(user_cookie.split('|')[0])
            _user_db_data = Users.get_by_id(user_id)
            username = _user_db_data.user_name
            self.render("index.html", username = username)
        else:
            self.redirect('/')

class Coursework(BaseHandler):
    def get(self):
        user_cookie = self.request.cookies.get('user_id')
        if user_cookie != '':
            user_id = int(user_cookie.split('|')[0])
            _user_db_data = Users.get_by_id(user_id)
            username = _user_db_data.user_name
            self.render("course_work.html", username = username)
        else:
            self.redirect('/')

class HelloUdacity(BaseHandler):
    def get(self):
        self.render("hello.html")
         
app = webapp2.WSGIApplication([('/homework', Homework),
                               ('/course_work', Coursework),
                               ('/unit1/helloudacity', HelloUdacity)
], debug=True)
