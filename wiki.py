import webapp2
from main import BaseHandler
from database import Wiki_Entries
import utils

class WikiPage(BaseHandler):
    def get(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                self.render("wiki_page.html", user = globals.users)
            else:
                get_user = utils.check_cookie(self)
                globals.users = get_user
                self.render("wiki_page.html", user = globals.users)
        else:
            self.redirect('/wiki/login')
        
class WikiEdit(BaseHandler):
    def get(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                
                content = utils.get_wiki_content()
                if content:   
                    self.render("wiki_edit.html", content = content, user = globals.users)
                else:
                    self.render("wiki_edit.html", user = globals.users)
        else:
            self.redirect("/wiki/login")
        
    def post(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                content = self.request.get("content")
                
                if content:
                    current_url = self.request.url.split('/')[-1]
                    if current_url == '_edit':
                        title = ''
                    else:
                        title = current_url
                    c = Wiki_Entries(content = content, title = title)
                    c.put()
                    self.redirect("/wiki/?" + title)
                else:
                    error = 'You must have content to save!'
                    self.render("wiki_edit.html", user = globals.users, error = error)
            else:
                self.redirect('/wiki/login')
        

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/wiki/_edit/(?:[a-zA-Z0-9_-]+/?)*', WikiEdit),
                               ('/wiki/(?:[a-zA-Z0-9_-]+/?)*', WikiPage)
], debug=True)