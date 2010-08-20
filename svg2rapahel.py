import os
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from svg.convert.raphael import Raphael

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/xhtml+xml'
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))

class Convert(webapp.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/javascript'
        raphael = Raphael(self.request.get('svg'))
        self.response.out.write(raphael.to_raphael())

application = webapp.WSGIApplication([
      ('/',        MainPage),
      ('/convert', Convert),
], debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
