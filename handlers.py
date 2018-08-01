import jinja2, datetime
import webapp2, os

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class BaseHandler(webapp2.RequestHandler):
	def render_template(self, filename, params={}):
		template = JINJA_ENVIRONMENT.get_template(filename)
		self.response.out.write(template.render(params))

class MainHandler(BaseHandler):
	def get(self):
		self.render_template('templates/home.html')

class ResultsHandler(BaseHandler):
    def post(self):
        query = self.request.get('query')
        params = { 'query': query }
        self.render_template('templates/results.html', params)
