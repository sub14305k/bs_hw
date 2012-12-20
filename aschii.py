import webapp2
from main import BaseHandler
from google.appengine.ext import db
from database import Art
import utils

class ASCIIChan(BaseHandler):

    def render_ASCII_page(self, title="", art = "", error = ""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")

        #prevent the running of multiple queries
        arts = list(arts)

        #find which arts have coords
        # points = []
        # for a in arts:
        #     if arts.coords:
        #         points.append(a.coords)
        points = filter(None, (a.coords for a in arts))

        img_url = None
        if points:
            img_url = utils.gmaps_img(points)

        self.render("ASCIIChan.html", title = title, art = art, error = error, arts = arts, img_url = img_url)

    def get(self):
        self.render_ASCII_page()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if art and title:
            a = Art(title = title, art = art)
            coords = utils.get_coords(self.request.remote_addr)
            if coords:
                a.coords = coords

            a.put()

            self.redirect("/course_work/unit3/ASCIIChan")
        else:
            error = "We need both title and some artwork!"
            self.render_ASCII_page(title,art,error) 

app = webapp2.WSGIApplication([('/course_work/unit3/ASCIIChan', ASCIIChan)                       
], debug=True)