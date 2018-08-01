import webapp2
from handlers import MainHandler, ResultsHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name='home'),
    webapp2.Route('/results', ResultsHandler, name='results'),
], debug=True)
