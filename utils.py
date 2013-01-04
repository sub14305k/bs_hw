import random
import string
import hashlib
import re
from google.appengine.ext import db
from google.appengine.api import memcache
from database import Users
import jinja2
import os
import hmac
import urllib2
#import json
from xml.dom import minidom
import logging

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

def check_cookie(self):
    user_cookie = self.request.cookies.get('user_id')
    if user_cookie and user_cookie != '':
        user_id = int(user_cookie.split('|')[0])
        _user_db_data = Users.get_by_id(user_id)
        user = _user_db_data.user_name
        return user
    else:
        return None
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

###C: Methods used in blog creation and JSON creation
    
def get_posts():
    posts = db.GqlQuery("SELECT * FROM Blog_db ORDER BY created DESC LIMIT 10")
    return posts

def get_post(post_id):
    key = db.Key.from_path('Blog_db', int(post_id), parent = blog_key())
    post = db.get(key)
    return post

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

def render(self):
    self._render_text = self.content.replace('\n', '<br>')
    return render_str("post.html", p = self)

def cache_blog(update = False):
    key = 'blog_front'
    posts = memcache.get(key)
    
    if posts is None or update:
        posts = get_posts()
        memcache.set(key,posts)
    return posts

def cache_permalink(post_id,post, update = False):
    key = post_id
    posts = memcache.get(key)
    
    if posts is None or update:
        posts = post
        memcache.set(key, posts)
    return posts
    
###C:END

###D: ASCHII_Chan 2 Geolocation

IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
    url = IP_URL + ip
    content = None
    coords = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return
    
    if content:
	    p = minidom.parseString(content)
            coords = p.getElementsByTagName("gml:coordinates")
        
            if coords and coords[0].childNodes[0].nodeValue:
               lon, lat = coords[0].childNodes[0].nodeValue.split(',')
               return db.GeoPt(lat, lon)

def top_arts(update = False):
    key = 'top'
    arts = memcache.get(key)
    if arts is None or update:
        logging.error("DB QUERY")
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")

        #prevent the running of multiple queries
        arts = list(arts)
        memcache.set(key, arts)
    return arts

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
def gmaps_img(points):
	markers = '&'.join('markers=%s,%s' % (p.lat, p.lon) for p in points)
	return GMAPS_URL + markers
###D:END


