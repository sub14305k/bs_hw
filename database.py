from google.appengine.ext import db
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Blog_db(db.Model):
        subject = db.StringProperty(required = True)
        content = db.TextProperty(required = True)
        created = db.DateTimeProperty(auto_now_add = True)
            
        def render_blog(self):
            self._render_text = self.content.replace('\n', '<br>')
            return render_str("post.html", p = self)

class Art(db.Model):
        title = db.StringProperty(required = True)
        art = db.TextProperty(required = True)
        created = db.DateTimeProperty(auto_now_add = True)

class Users(db.Model):
        user_email = db.StringProperty(required = False)
        user_name = db.StringProperty(required = True)
        user_pass = db.StringProperty(required = True)
        created_on = db.DateTimeProperty(auto_now_add = True)

