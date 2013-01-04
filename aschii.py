import webapp2
from main import BaseHandler
from google.appengine.ext import db
from google.appengine.api import memcache
from database import Art
from database import Users
import utils

class ASCIIChan(BaseHandler):

    def render_ASCII_page(self, title="", art = "", error = ""):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:

                arts = utils.top_arts()
                img_url = None
                points = filter(None, (a.coords for a in arts))
        
                if points:
                    img_url = utils.gmaps_img(points)
        
                self.render("ASCIIChan.html", title = title, art = art, error = error, arts = arts, img_url = img_url, user = globals.users)
        else:
            self.redirect('/')

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
            #rerun the query and update CACHE
            utils.top_arts(True)

            self.redirect("/course_work/unit3/ASCIIChan")
        else:
            error = "We need both title and some artwork!"
            self.render_ASCII_page(title,art,error) 

app = webapp2.WSGIApplication([('/course_work/unit3/ASCIIChan', ASCIIChan)                       
], debug=True)