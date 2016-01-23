#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Guestbook
import time

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        vnosi = Guestbook.query().fetch()
        params = {"vnosi":vnosi}
        return self.render_template("gosti.html", params)
    def post(self):
        ime = self.request.get("ime")
        if (len(ime) == 0):
            ime = "Neznanec"
        email = self.request.get("email")
        sporocilo = self.request.get("sporocilo")
        if (len(sporocilo) == 0 or len(sporocilo.strip(' ')) == 0):
            napaka = {"napaka":"Vsebina sporocila je potrebna!"}
            return self.render_template("gosti.html", napaka)
        vnos = Guestbook(ime=ime, email=email, sporocilo=sporocilo)
        vnos.put()
        #pridobivanje vseh vnosov
        vnosi = Guestbook.query().fetch()
        params = {"vnosi":vnosi}
        return self.render_template("gosti.html", params)

class VnosHandler(BaseHandler):
    def get(self, vnos_id):
        vnos = Guestbook.get_by_id(int(vnos_id))
        params = {"vnos":vnos}
        return self.render_template("vnos.html", params)

class UrediHandler(BaseHandler):
    def get(self, vnos_id):
        vnos = Guestbook.get_by_id(int(vnos_id))
        params = {"vnos":vnos}
        return self.render_template("uredi.html", params)
    def post(self, vnos_id):
        vnos = Guestbook.get_by_id(int(vnos_id))
        vrednost_vnosa = self.request.get("sporocilo")
        vnos.sporocilo = vrednost_vnosa
        vnos.put()
        time.sleep(0.1)
        return self.redirect_to("seznam-vnosov")

class BrisiHandler(BaseHandler):
    def get(self, vnos_id):

        vnos = Guestbook.get_by_id(int(vnos_id))
        params = {"vnos":vnos}
        return self.render_template("brisi.html", params)
    def post(self, vnos_id):
        vnos = Guestbook.get_by_id(int(vnos_id))
        vnos.key.delete()
        time.sleep(0.1)
        return self.redirect_to("seznam-vnosov")




app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name = "seznam-vnosov"),
    webapp2.Route('/vnos/<vnos_id:\d+>', VnosHandler),
    webapp2.Route('/vnos/uredi/<vnos_id:\d+>', UrediHandler),
    webapp2.Route('/vnos/brisi/<vnos_id:\d+>', BrisiHandler),
], debug=True)
