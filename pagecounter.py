import webapp2
from main import BaseHandler
from database import Users
import utils

class Page_Counter(BaseHandler):
	
	def get(self):
			valid_cookie = self.request.cookies.get('user_id')
			if valid_cookie:
				import globals
				if globals.users != None:
					visits = 0
					visits_cookie_val = self.request.cookies.get('visits')
					if visits_cookie_val:
						cookie_valid = utils.check_secure_val(visits_cookie_val)
						if cookie_valid:
							visits = int(cookie_valid)
				visits += 1
				
				new_cookie_val = utils.make_secure_val(str(visits))	
				
				self.response.headers.add_header('Set-Cookie', 'visits=%s;Path=/' % new_cookie_val) 
				self.render("page_visits.html", visits = visits, user = globals.users)
			else:
				self.redirect('/')

app = webapp2.WSGIApplication([('/course_work/unit4/pagecounter', Page_Counter)
], debug=True)