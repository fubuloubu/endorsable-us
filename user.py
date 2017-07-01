from database import Database

class User(Database):
    def __init__(self):
        Database.__init__(self)
    
    def get_user_name(self, user_uid):
        return self._get_db_data('users/' + user_uid + '/name')

    def get_user_data(self, user_uid):
        userdata = self._get_db_data('users/' + user_uid)
        # Don't give out contact information
        if self.get_uid() != user_uid:
            del userdata['email']
        userdata['uid'] = user_uid
        friends = self.get_relationships_by_uid(user_uid)
        if friends: # User has friends
            #Add name from key, change value to type
            for friend in friends:
                friend['name'] = self.get_user_name(friend['uid'])
            userdata['relationships'] = friends
        return userdata

    def add_relationship(self, friend_uid, relationship='friend'):
        # Dual pointer relationship
        self._set_db_data('relationships/' + self.get_uid() + \
                '/' + friend_uid, relationship)
        self._set_db_data('relationships/' + friend_uid + \
                '/' + self.get_uid(), relationship)

    def get_relationships_by_uid(self, user_uid):
        return self._get_db_array('relationships/' + user_uid, valname='type', keyname='uid')

    def get_user_relationships(self):
        return self.get_relationships_by_uid(self.get_uid())

    def get_endorsements_by_uid(self, user_uid):
        endorsements = self._get_db_array('endorsements/' + user_uid)
        user_name = self.get_user_name(user_uid)
        for endr in endorsements:
            endr['toname'] = user_name
            endr['fromname'] = self.get_user_name(endr['from'])
        return endorsements

    def get_user_endorsements(self):
        return self.get_endorsements_by_uid(self.get_uid())

    def get_all_endorsements(self):
        # User + Friends
        endorsements = []
        endorsements.extend(self.get_user_endorsements())
        friends = self.get_user_relationships()
        if friends: # User has friends
            for friend in friends:
                endorsements.extend(self.get_endorsements_by_uid(friend['uid']))
        return endorsements

    def get_pending_endorsements(self):
        return self._get_db_array('pending/' + self.get_uid())

    def add_endorsement(self, uid_to, endorsement_text, time):
        endorsement = {
            "text" : endorsement_text,
            "from" : self.get_uid(),
            "time" : time,
            "to"   : uid_to, # This is used to keep track of the
                             # final approver, aka which user can
                             # publish the endorsement
        }
        self._push_db_array('pending/' + uid_to, endorsement)

    def accept_pending(self, pending_uid):
        endorsement = self._pop_db_array('pending/' + self.get_uid() + '/' + pending_uid)
        if endorsement:
            uid_to = endorsement['to']
            del endorsement['to']
            self._push_db_array('endorsements/' + uid_to, endorsement)

    def amend_pending(self, pending_uid, updated_text):
        endorsement = self._pop_db_array('pending/' + self.get_uid() + '/' + pending_uid)
        if endorsement:
            endorsement['text'] = updated_text
            next_uid = endorsement['from'] if endorsement['to'] == self.get_uid() else endorsement['to']
            self._push_db_array('pending/' + next_uid, endorsement)

    def reject_pending(self, pending_uid):
        self._pop_db_array('pending/' + self.get_uid() + '/' + pending_uid)
