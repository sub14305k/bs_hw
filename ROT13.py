import webapp2
from main import BaseHandler

rot_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
rot_list2 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def ROT13(s):
    replaced_string = []
    for char in s:
        if char not in rot_list and char not in rot_list2:
            replaced_string += char
        if char in rot_list:
            index = rot_list.index(char)
            if index < 13:
                replaced_string += rot_list[index + 13]
            if index >= 13:
                replaced_string += rot_list[index - 13]
        if char in rot_list2:
            index = rot_list2.index(char)
            if index < 13:
                replaced_string += rot_list2[index + 13]
            if index >= 13:
                replaced_string += rot_list2[index - 13]
    replaced_string = ''.join(replaced_string)
    return replaced_string

class Rot13(BaseHandler):
    
    def get(self):
        self.render("rot13-form.html")
    def post(self):
        user_input = self.request.get("text")
        if user_input == "":
            self.render("rot13-form.html", error = "You didn't enter any text. Please try again.")
        else:  
          convert = ROT13(user_input)
          self.render("rot13-form.html",user_input = convert)

app = webapp2.WSGIApplication([('/unit2/rot13', Rot13)
], debug=True)