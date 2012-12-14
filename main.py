import webapp2
import os
import jinja2

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

def render(self):
    self._render_text = self.content.replace('\n', '<br>')
    return render_str("post.html", p = self)

class Homework(BaseHandler):
    def get(self):
        self.render("index.html")

class Coursework(BaseHandler):
    def get(self):
        self.render("course_work.html")

class HelloUdacity(BaseHandler):
    def get(self):
        self.render("hello.html")
         
app = webapp2.WSGIApplication([('/homework', Homework),
                               ('/course_work', Coursework),
                               ('/unit1/helloudacity', HelloUdacity)
], debug=True)
