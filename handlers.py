from models import User, Pet
from webapp2_extras import auth, sessions

import jinja2
import os
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user(self):
        return User.get_by_id(self.user_info['user_id']) if self.user_info else None

    @webapp2.cached_property
    def user_id(self):
        return self.user_info['user_id'] if self.user_info else None

    def render_template(self, filename, params={}):
        print(self.user_info)
        print('kkk')
        user_info = self.user_info
        if user_info:
            user = User.get_by_id(int(user_info['user_id']))
            params['user'] = user
        else:
            params['user'] = None
        template = JINJA_ENVIRONMENT.get_template(filename)
        self.response.out.write(template.render(params))

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

class MainHandler(BaseHandler):
    def get(self):
        params = { 'home': True }
        self.render_template('templates/home.html', params)

class LoginHandler(BaseHandler):
    def get(self):
        if self.user_info:
            self.redirect_to('home')
            return
        self.auth.unset_session()
        self.render_template('templates/login.html')

    def post(self):
        self.auth.unset_session()
        email = self.request.get('email').lower()
        password = self.request.get('password')
        if not email or not password:
            self.auth.unset_session()
            self.redirect_to('login')
            return
        try:
            self.auth.get_user_by_password(email, password, remember=True)
            print(self.user_info)
            if not self.user_info:
                self.redirect_to('login')
            else:
                self.redirect_to('home')
        except:
            self.auth.unset_session()
            self.redirect_to('login')

class SignupHandler(BaseHandler):
    def get(self):
        if self.user_info:
            self.redirect_to('home')
        else:
            self.render_template('templates/signup.html')

    def post(self):
        self.auth.unset_session()
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        email_address = self.request.get('email').lower()
        password = self.request.get('password')

        if User.query(User.email_address == email_address).fetch():
            self.redirect_to('signup')
            return

        unique_properties = ['email_address']
        user_data = self.auth.store.user_model.create_user(
            email_address,
            unique_properties,
            email_address=email_address,
            password_raw=password
        )

        if not user_data[0]:
            self.redirect_to('signup')
            return

        user = user_data[1]
        user.first_name = first_name
        user.last_name = last_name
        user.email_address = email_address
        user.put()

        self.redirect_to('login')

class LogoutHandler(BaseHandler):
    def get(self):
        self.auth.unset_session()
        self.redirect_to('home')

class SearchHandler(BaseHandler):
    def get(self):
        self.render_template('templates/search.html')

class ResultsHandler(BaseHandler):
    def post(self):
        query = self.request.get('query')
        pets = list()
        for pet in Pet.query().fetch():
            for keyword in query.split():
                if keyword in pet.keywords:
                    pets.append(pet)
                    break
        params = {
            'query': query,
            'pets': pets,
        }
        self.render_template('templates/results.html', params)

class ListHandler(BaseHandler):
    def get(self):
        self.render_template('templates/list.html')

    def post(self):
        name = self.request.get('name')
        breed = self.request.get('breed')
        sex = self.request.get('sex')
        birth_date = self.request.get('birth')
        city = self.request.get('city')
        description = self.request.get('description')
        keywords_str = self.request.get('keywords')
        keywords = list()
        for keyword in keywords_str.split(','):
            keywords.append(keyword.strip())

        # TODO: FIGURE OUT WHERE TO UPLOAD PICTURE TO
        # picture = self.request.POST.multi['picture']
        # picture_data = picture.value
        # image_url = ???

        image_url = '/img/golden-retriever.jpg'

        Pet.create(
            owner=self.user.key,
            breed=breed,
            sex=sex,
            keywords=keywords,
            name=name,
            birth_date=birth_date,
            city=city,
            description=description,
            image_url=image_url,
        )

        self.redirect_to('home')

class ListingHandler(BaseHandler):
    def get(self, **kwargs):
        pet_id = kwargs['pet_id']
        pet = Pet.get_by_id(long(pet_id))
        params = {
            'pet': pet,
            'owner': pet.owner.get()
        }
        self.render_template('templates/listing.html', params)

class PetsHandler(BaseHandler):
    def get(self):
        if not self.user_info:
            self.redirect_to(('login'))
            return
        pets = Pet.query(Pet.owner == self.user.key).fetch()
        params = {
            'pets': pets,
        }
        self.render_template('templates/pets.html', params)

class PetHandler(BaseHandler):
    def get(self, **kwargs):
        pet_id = kwargs['pet_id']
        pet = Pet.get_by_id(long(pet_id))
        params = {
            'pet': pet,
            'owner': pet.owner.get()
        }
        self.render_template('templates/pet.html', params)
