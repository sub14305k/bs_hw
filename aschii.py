import webapp2
from main import BaseHandler
from google.appengine.ext import db
from database import Art

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

app = webapp2.WSGIApplication([('/course_work/unit3/ASCIIChan', ASCIIChan)                       
], debug=True)