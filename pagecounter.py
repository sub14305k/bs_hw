import webapp2
from main import BaseHandler
import utils

class Page_Counter(BaseHandler):
	def get(self):
		visits = 0
		visits_cookie_val = self.request.cookies.get('visits')
		if visits_cookie_val:
			cookie_valid = utils.check_secure_val(visits_cookie_val)
			if cookie_valid:
				visits = int(cookie_valid)
		
		visits += 1

		new_cookie_val = utils.make_secure_val(str(visits))

		self.response.headers.add_header('Set-Cookie', 'visits=%s;Path=/' % new_cookie_val) 
		self.render("page_visits.html", visits = visits)

app = webapp2.WSGIApplication([('/course_work/unit4/pagecounter', Page_Counter)
], debug=True)
