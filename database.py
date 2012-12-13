from google.appengine.ext import db
from main import render_str

class Blog_db(db.Model):
        subject = db.StringProperty(required = True)
        content = db.TextProperty(required = True)
        created = db.DateTimeProperty(auto_now_add = True)

        def render(self):
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

