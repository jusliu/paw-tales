import webapp2
from handlers import MainHandler, LoginHandler, SignupHandler, LogoutHandler, ResultsHandler, ListHandler, ListingHandler

config = {
	'webapp2_extras.sessions': {
		'secret_key': 'paw-tales',
		'backends': {
			'securecookie': 'webapp2_extras.sessions.SecureCookieSessionFactory',
			'datastore': 'webapp2_extras.appengine.sessions_ndb.DatastoreSessionFactory',
			'memcache': 'webapp2_extras.appengine.sessions_memcache.MemcacheSessionFactory',
		}
	}
}

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name='home'),
    webapp2.Route('/login', LoginHandler, name='login'),
    webapp2.Route('/signup', SignupHandler, name='signup'),
    webapp2.Route('/logout', LogoutHandler, name='logout'),
    webapp2.Route('/results', ResultsHandler, name='results'),
    webapp2.Route('/list', ListHandler, name='list'),
    webapp2.Route('/listing/<pet_id:.+>', ListingHandler, name='listing'),
], debug=True, config=config)
