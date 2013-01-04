import webapp2
from main import BaseHandler
from database import Users
import utils

class Rot13(BaseHandler):
    
    def get(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                self.render("rot13-form.html", user = globals.users)
        else:
            self.redirect('/')
            
    def post(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
            
                user_input = self.request.get("text")
                if user_input == "":
                    self.render("rot13-form.html", error = "You didn't enter any text. Please try again.", user = globals.users)
                else:  
                  convert = utils.ROT13(user_input)
                  self.render("rot13-form.html",user_input = convert, user = globals.users)
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([('/unit2/rot13', Rot13)
], debug=True)