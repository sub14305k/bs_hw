import webapp2
from main import BaseHandler
import utils

class Rot13(BaseHandler):
    
    def get(self):
        self.render("rot13-form.html")
    def post(self):
        user_input = self.request.get("text")
        if user_input == "":
            self.render("rot13-form.html", error = "You didn't enter any text. Please try again.")
        else:  
          convert = utils.ROT13(user_input)
          self.render("rot13-form.html",user_input = convert)

app = webapp2.WSGIApplication([('/unit2/rot13', Rot13)
], debug=True)