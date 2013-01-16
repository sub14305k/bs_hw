from google.appengine.ext import db
import utils

class Blog_db(db.Model):
        subject = db.StringProperty(required = True)
        content = db.TextProperty(required = True)
        created = db.DateTimeProperty(auto_now_add = True)
            
        def render_blog(self):
            self._render_text = self.content.replace('\n', '<br>')
            return utils.render_str("post.html", p = self)
        
        def create_dict(self):
            d = { 'subject': self.subject,
                  'content': self.content,
                  'created': str(self.created)
                 }
            return d

class Art(db.Model):
        title = db.StringProperty(required = True)
        art = db.TextProperty(required = True)
        created = db.DateTimeProperty(auto_now_add = True)
        coords = db.GeoPtProperty()

class Users(db.Model):
        user_email = db.StringProperty(required = False)
        user_name = db.StringProperty(required = True)
        user_pass = db.StringProperty(required = True)
        created_on = db.DateTimeProperty(auto_now_add = True)
        
class Wiki_Entries(db.Model):
        content = db.TextProperty(required = True)
        title = db.StringProperty(required = True)
        created = db.DateTimeProperty(auto_now_add = True)

        def render_history(self):
            self._render_text = self.content.replace('\n', '')
            return utils.render_str("history_edits.html", p = self)
        
        def create_dict_wiki(self):
            d = {'title': self.title,
                 'content': self.content,
                 'created': str(self.created)
                 }
            return d

        


