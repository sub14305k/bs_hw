import webapp2
from main import BaseHandler
from database import Blog_db
from google.appengine.ext import db

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

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

app = webapp2.WSGIApplication([('/blog/?', Blog_Page),
                               ('/blog/newpost', Create_Blog),
                               ('/blog/([0-9]+)', Permalink)
], debug=True)