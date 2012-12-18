import webapp2
from main import BaseHandler
# import hashlib
import hmac

SECRET = 'supersecret'

def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return s + '|' + hash_str(s)

def check_secure_val(h):
    find_split = h.find('|')
    if hash_str(h[:find_split]) == h[find_split + 1:]:
        return h[:find_split]
    else:
        return None

class Page_Counter(BaseHandler):
	def get(self):
		visits = 0
		visits_cookie_val = self.request.cookies.get('visits')
		if visits_cookie_val:
			cookie_valid = check_secure_val(visits_cookie_val)
			if cookie_valid:
				visits = int(cookie_valid)
		
		visits += 1

		new_cookie_val = make_secure_val(str(visits))

		self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val) 
		self.render("page_visits.html", visits = visits)

app = webapp2.WSGIApplication([('/course_work/unit4/pagecounter', Page_Counter)
], debug=True)
