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
        
    def _get_db_data(self, key):
        return self._db.child(key).get(self._id_token).val()

    def _set_db_data(self, key, data):
        self._db.child(key).set(data, self._id_token)

    def _upd_db_data(self, key, data):
        self._db.child(key).update(data, self._id_token)
        
    def _del_db_data(self, key):
        return self._db.child(key).remove(self._id_token)

    def _push_db_data(self, key, data):
        self._db.child(key).push(data, self._id_token)

    def _pop_db_data(self, key):
        data = self._get_db_data(key)
        self._del_db_data(key)
        return data
        
    def get_uid(self):
        if self._uid is not None:
            return self._uid
        return ''
        
    # Perform a login
    def login(self, email, password):
        try:
            user = self._auth.sign_in_with_email_and_password(email, password)
            self._set_auth_data(user)
            return None if self.authenticated() else 'Not sure what happened here...'
        except request_exceptions.HTTPError as error:
            #'Your password is incorrect or you are not registered in the system' + \
            #        '<br><br>You can register ' + create_link('register', 'here')
            return error # Login unsuccessful

    def register(self, fullname, email, password):
        try:
            user = self._auth.create_user_with_email_and_password(email, password)
            self._set_auth_data(user)
            # Add user data to our db
            userdata = {"email": email, "name": fullname}
            self._set_db_data('users', {self.get_uid() : userdata})
            return None if self.authenticated() else 'Not sure what happened here...'
        except request_exceptions.HTTPError as error:
            #'The email you provided is already in use' + \
            #        '<br><br>You can login ' + create_link('login', 'here')
            return error # Registration unsuccessful

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

    def get_user_data(self, user_uid):
        return self._get_db_data('users/' + user_uid)

    def get_user_relationships(self):
        return self._get_db_data('relationships/' + self.get_uid())

    def get_endorsements_by_uid(self, user_uid):
        return self._get_db_data('endorsements/' + user_uid)

    def get_user_endorsements(self):
        return self.get_endorsements_by_uid(self.get_uid())

    def get_pending_endorsements(self):
        return self._get_db_data('pending/' + self.get_uid())

    def add_endorsement(self, uid_to, endorsement_text, time):
        endorsement = {
            "text" : endorsement_text,
            "from" : self.get_uid(),
            "time" : time,
            "to"   : uid_to, # This is used to keep track of the
                             # final approver, aka which user can
                             # publish the endorsement
        }
        self._push_db_data('pending/' + uid_to, endorsement)

    def accept_pending(self, pending_uid):
        endorsement = self._pop_db_data('pending/' + self.get_uid() + '/' + endorsement_uid)
        uid_to = endorsement['to']
        del endorsement['to']
        self._push_db_data('endorsements/' + uid_to, endorsement)

    def amend_pending(self, pending_uid, updated_text):
        endorsement = self._pop_db_data('pending/' + self.get_uid() + '/' + endorsement_uid)
        uid_to = endorsement['to']
        endorsement['text'] = updated_text
        self._push_db_data('pending/' + uid_to, endorsement)

    def reject_pending(self, pending_uid):
        self._pop_db_data('pending/' + self.get_uid() + '/' + endorsement_uid)
