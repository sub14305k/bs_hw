import random
import string
import hashlib
import re
from google.appengine.ext import db
import jinja2
import os
import hmac
import urllib2
from xml.dom import minidom

###0:Jinja Template Method
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
###0:END


###A: Utility methods used in verification of username & passwords / encrypting for security
SECRET = 'nl;ajkdfnHJKsHJh56dafdfasfsd'

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

def make_salt():
    make_characters = string.letters
    return ''.join(random.sample(make_characters,5))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h,salt)

def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASS_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)
###A:END

###B: Method used to convert strings using ROT13 encoding
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
###B:END

###C: Methods used in blog creation
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

def render(self):
    self._render_text = self.content.replace('\n', '<br>')
    return render_str("post.html", p = self)
###C:END

###D: ASCHII_Chan 2 Geolocation

IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
	ip = "4.2.2.2"
	url = IP_URL + ip
	content = urllib2.urlopen(url).read()
	if content:
		p = minidom.parseString(content)
    	coords = p.getElementsByTagName("gml:coordinates")
    	if coords and coords[0].childNodes[0].nodeValue:
        	lon, lat = coords[0].childNodes[0].nodeValue.split(',')
    	return db.GeoPt(lat, lon)

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
def gmaps_img(points):
	markers = '&'.join('markers=%s,%s' % (p.lat, p.lon) for p in points)
	return GMAPS_URL + markers



