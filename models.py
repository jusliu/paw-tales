import time
import webapp2_extras.appengine.auth.models
from google.appengine.ext import ndb
from webapp2_extras import security

class User(webapp2_extras.appengine.auth.models.User):
    email_address = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)

    def set_password(self, raw_password):
        self.password = security.generate_password_hash(raw_password, length=12)

    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp
        return None, None

class Pet(ndb.Model):
    owner = ndb.KeyProperty(kind='User')
    breed = ndb.StringProperty()
    sex = ndb.StringProperty()
    keywords = ndb.StringProperty(repeated=True)
    name = ndb.StringProperty()
    birth_date = ndb.StringProperty()
    city = ndb.StringProperty()
    description = ndb.StringProperty()
    image_url = ndb.StringProperty()

    @classmethod
    def create(cls, owner, breed, sex, keywords, name, birth_date, city, description, image_url):
        pet = cls(
            owner=owner,
            breed=breed,
            sex=sex,
            keywords=keywords,
            name=name,
            birth_date=birth_date,
            city=city,
            description=description,
            image_url=image_url,
        )
        pet.put()
        return pet
