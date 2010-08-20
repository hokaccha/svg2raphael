import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'application/xhtml+xml'
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, {}))

class Convert(webapp.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/javascript'
    self.response.out.write('console.log("hoge")')

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/convert', Convert),
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
