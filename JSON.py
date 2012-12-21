import webapp2
from main import BaseHandler
from google.appengine.ext import db

class JSON(BaseHandler):
    def get(self):
        entries = db.GqlQuery("SELECT * FROM Blog_db ORDER BY created")
        listBlog = []
        for posts in entries:
        	listBlog.append('{"content":"%s", "subject":"%s","created":"%s"}' % (posts.content,posts.subject,posts.created))
        JSON_string = ','.join(listBlog)
        self.render("blog_json.html", content = JSON_string)

app = webapp2.WSGIApplication([('/blog.json', JSON)
], debug=True)