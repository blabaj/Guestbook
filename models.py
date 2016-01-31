from google.appengine.ext import ndb
from google.appengine.api import users


class  Guestbook(ndb.Model):
    ime = ndb.StringProperty()
    email = ndb.StringProperty()
    sporocilo = ndb.TextProperty()
    datum_komentarja = ndb.DateTimeProperty(auto_now_add=True)