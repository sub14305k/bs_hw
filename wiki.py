import webapp2
from main import BaseHandler
from database import Wiki_Entries
from google.appengine.ext import db
from google.appengine.api import memcache
import utils

class WikiPage(BaseHandler):
    def get(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                url = self.request.url.split('/')
                build_edit_url = '/' + url[-2] + '/_edit/' + url[-1]
                build_history_url = '/' + url[-2] + '/history/' + url[-1]
                url_title = self.request.url.split('/')[-1]
                if not url_title:
                    url_title = 'welcome'
                stored = memcache.get(url_title)
                if stored is not None:
                    self.render("wiki_page.html", user = globals.users, content = stored, build_url = build_edit_url, history_url = build_history_url)
                else:
                    check_exist = utils.get_wiki_content()
                    content = None
                    for entry in check_exist:
                        title = entry['title']
                        if title == url_title:
                            content = entry['content']
                    if content:
                        content =  content
                        utils.cache_wiki(url_title, content, True)
                        self.render("wiki_page.html", content = content, user = globals.users, build_url= build_edit_url, history_url = build_history_url)
                    else:
                        self.redirect('/wiki/_edit/' + url_title)
                    
            else:
                get_user = utils.check_cookie(self)
                globals.users = get_user
                url = self.request.url.split('/')
                build_edit_url = '/' + url[-2] + '/_edit/' + url[-1]
                build_history_url = '/' + url[-2] + '/history/' + url[-1]
                url_title = self.request.url.split('/')[-1]
                if not url_title:
                    url_title = 'welcome'
                stored = memcache.get(url_title)
                if stored is not None:
                    self.render("wiki_page.html", user = globals.users,content = stored, build_url = build_edit_url, history_url = build_history_url)
                else:
                    if url_title == 'welcome':
                        check_exist = utils.get_wiki_content()
                        content = None
                        for entry in check_exist:
                            title = entry['title']
                            if title == url_title:
                                content = entry['content']
                        if content:
                            content =  content
                            utils.cache_wiki(url_title, content, True)
                            self.render("wiki_page.html", content = content, user = globals.users, build_url= build_edit_url, history_url = build_history_url)
                        else:
                            self.redirect('/wiki/_edit/')
                    else:
                        self.redirect('/wiki/_edit/' + url_title)
        else:
            self.redirect('/wiki/login')
        
class WikiEdit(BaseHandler):
    def get(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                url_title = self.request.url.split('/')[-1]
                if not url_title:
                    url_title = 'welcome'
                content = memcache.get(url_title)
                if content:   
                    self.render("wiki_edit.html", content = content, user = globals.users, current_url = url_title)
                else:
                    self.render("wiki_edit.html", user = globals.users)
        else:
            self.redirect("/wiki/login")
        
    def post(self):
                url_title = self.request.url.split('/')[-1]
                if not url_title:
                    url_title = 'welcome'
                stored_content = memcache.get(url_title)
                content = self.request.get("content")
                
                if content and content != stored_content:
                        if not url_title:
                            title = 'welcome'
                        else:
                            title = url_title
                        if stored_content:
                            c = Wiki_Entries(parent = utils.wiki_key(title), content = content, title = title)
                        else:
                            c = Wiki_Entries(key_name = title, content = content, title = title)
                        c.put()
                        utils.cache_wiki(title, content, True)

                        if title == 'welcome':
                            self.redirect("/wiki/")
                        else:
                            self.redirect("/wiki/" + title)

                else:
                    if title == 'welcome':
                        self.redirect('/wiki/')
                    else:
                        self.redirect('/wiki/' + title)
                        
class Wiki_History(BaseHandler):
    def get(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                url_title = self.request.url.split('/')[-1]
                if not url_title:
                    url_title = 'welcome'
                history = memcache.get(url_title + '_history')
                # key = db.Key.from_path('Wiki_Entries', url_title)
                if not history:
                    history = utils.get_wiki_history(url_title)
                # test = history
                # self.render("test.html", test = test)
                self.render("history_main.html", history = history, user = globals.users)
        else:
            self.redirect("/wiki/login")
           
PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/wiki/_edit/(?:[a-zA-Z0-9_-]+/?)*', WikiEdit),
                               ('/wiki/history/(?:[a-zA-Z0-9_-]+/?)*', Wiki_History),
                               ('/wiki/(?:[a-zA-Z0-9_-]+/?)*', WikiPage)
                               
], debug=True)