import os
import logging
import re
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from svg.convert.raphael import Raphael

class MainPage(webapp.RequestHandler):
    def get(self):
        content_type = 'application/xhtml+xml'
        match = re.search('MSIE ([\d\.]+);', self.request.headers['User-Agent'])
        if match and float(match.group(1)) < 8:
            content_type = 'text/html'
        self.response.headers['Content-Type'] = content_type

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {
            'content_type': content_type
        }))

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
