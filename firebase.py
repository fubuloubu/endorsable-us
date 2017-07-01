import pyrebase
from requests import exceptions as request_exceptions
class User(object):
    def __init__(self):
        config = {
            "apiKey" : "AIzaSyCGxsg4BmTj3q9ZT8y9c-hhbQ6wW8ehv9g",
            "authDomain" : "endorsable-9fa55.firebaseapp.com",
            "databaseURL" : "https://endorsable-9fa55.firebaseio.com",
            #"projectId" : "endorsable-9fa55",
            "storageBucket" : "endorsable-9fa55.appspot.com",
            #"messagingSenderId" : "660294942426"
        }
        firebase = pyrebase.initialize_app(config)
        self._auth = firebase.auth()
        self._db = firebase.database()
        self._uid = None
        self._id_token = None
        self._refresh_token = None
    
    def _set_auth_data(self, user):
        self._uid = user['localId']
        self._id_token = user['idToken']
        self._refresh_token = user['refreshToken']
        self._timeout = user['expiresIn']

    def _set_db_data(self, key, data):
        self._db.child(key).set(data, self._id_token)

    def get_uid(self):
        if self._uid is not None:
            return self._uid
        return ''
        
    # Perform a login
    def login(self, email, password):
        try:
            user = self._auth.sign_in_with_email_and_password(email, password)
            self._set_auth_data(user)
            return self.authenticated()
        except request_exceptions.HTTPError as e:
            return False # Login unsuccessful

    def register(self, fullname, email, password):
        try:
            user = self._auth.create_user_with_email_and_password(email, password)
            self._set_auth_data(user)
            # Add user data to our db
            userdata = {"email": email, "name": fullname}
            self._set_db_data('users', {self.get_uid() : userdata})
            return self.authenticated()
        except request_exceptions.HTTPError as e:
            return False # Registration unsuccessful

    def _refresh_session(self):
        user = self._auth.refresh(self.refresh_token)
        self._id_token = user['idToken']
        self._refresh_token = user['refreshToken']

    # Check if session token is active
    def _is_session_expired(self):
        return self._refresh_token is None
        
    # User has authenticated and has an active session token
    def authenticated(self):
        return self._id_token is not None and not self._is_session_expired()
