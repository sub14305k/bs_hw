import webapp2
from main import BaseHandler
from database import Blog_db
from google.appengine.ext import db
from google.appengine.api import memcache
from database import Users
import utils
import datetime

time_start_blog = datetime.datetime.now()

class Blog_Page(BaseHandler):
        
    def get(self):

        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
            
                
                global time_start_blog;
                posts = memcache.get('blog_front')
                if not posts:
                    posts = utils.cache_blog()
                    time_start_blog = datetime.datetime.now()
        
                time_reload = datetime.datetime.now()
                total_time = time_reload - time_start_blog
                seconds = total_time.seconds
                sec_time = 'Queried: %s seconds ago' % seconds
                self.render("blog.html", posts = posts, time = sec_time, user = globals.users)
        else:
            self.redirect('/')
   
class Create_Blog(BaseHandler):
    
    def get(self):
        
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                self.render("newpost.html", user = globals.users)
        else:
            self.redirect('/')
            
    def post(self):
        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
                subject = self.request.get("subject")
                contents = self.request.get("content")
        
                if subject and contents:
                    s = Blog_db(parent = utils.blog_key(), subject = subject, content = contents)
                    s.put()
                    utils.cache_blog(True)
        
                    self.redirect("/blog/%s" % str(s.key().id()))
                else:
                    error = "We need both subject and content!"
                    self.render("newpost.html", subject = subject, content = contents, error = error, user = globals.users)
        else:
            self.redirect('/')

time_start_post = datetime.datetime.now()
class Permalink(BaseHandler):

     def get(self,post_id):

        valid_cookie = self.request.cookies.get('user_id')
        if valid_cookie:
            import globals 
            if globals.users != None:
            
                global time_start_post;
                post = memcache.get(post_id)
                
                if not post:
                    post = utils.get_post(post_id)
                    time_start_post = datetime.datetime.now()
                    utils.cache_permalink(post_id, post, True)
                     
                time_reload = datetime.datetime.now()
                total_time = time_reload - time_start_post
                seconds = total_time.seconds
                sec_time = 'Queried: %s seconds ago' % seconds
                
                if not post:
                    self.error(404)
                    return
        
                self.render("permalink.html", post = post, time = sec_time, user= globals.users)
        else:
            self.redirect('/')

class Blog_JSON(BaseHandler):
    def get(self):
         content = utils.get_posts()
         self.render_json([p.create_dict() for p in content])

class Permalink_JSON(BaseHandler):
    def get(self, post_id):
        
        post = utils.get_post(post_id)
        self.render_json(post.create_dict())
        
class Cache_Flush(BaseHandler):
    def get(self):
        memcache.flush_all()
        self.redirect("/blog")
        
app = webapp2.WSGIApplication([('/blog/?', Blog_Page),
                               ('/blog/newpost', Create_Blog),
                               ('/blog/([0-9]+)', Permalink),
                               ('/blog.json', Blog_JSON),
                               ('/blog/([0-9]+).json', Permalink_JSON),
                               ('/blog/flush', Cache_Flush)
], debug=True)