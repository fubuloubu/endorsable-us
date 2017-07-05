from database import Database

class BasicUser(Database):
    def __init__(self):
        Database.__init__(self)
    
    # Getters
    def get_user_name(self, user_uid):
        return self._get_db_data('users/' + user_uid + '/name')

    def get_name(self):
        return self.get_user_name(self.get_uid())
    
    def get_user_relationships(self, user_uid):
        friends = self._get_db_array('relationships/' + user_uid, valname='type', keyname='uid')
        if friends: # User has friends
            #Add name from key, change value to type
            for friend in friends:
                friend['name'] = self.get_user_name(friend['uid'])
        return friends

    def get_relationships(self):
        return self.get_user_relationships(self.get_uid())

    def get_relationship_type(self, user_uid):
        return self._get_db_data('relationships/' + self.get_uid() + '/' + user_uid)
    
    def is_me(self, user_uid):
        return user_uid == self.get_uid()
    
    def is_connected(self, user_uid):
        return user_uid in [r['uid'] for r in self.get_relationships()]

    def get_all_users(self):
        all_users = self._get_db_array('users', keyname='uid')
        # Remove self
        all_users = list(filter(lambda u: not self.is_me(u['uid']), all_users))
        for u in all_users:
            # Add if connected
            if self.is_connected(u['uid']):
                u['relationship_type'] = self.get_relationship_type(u['uid'])
        return all_users

    def get_pending_endorsements(self):
        endorsements = self._get_db_array('pending/' + self.get_uid())
        for endr in endorsements:
            endr['fromname'] = self.get_user_name(endr['from'])
        return endorsements
    
    # Actions
    def add_relationship(self, formdata):
        friend_uid = formdata['friend_uid']
        relationship = formdata['relationship']
        # Dual pointer relationship
        self._set_db_data('relationships/' + self.get_uid() + \
                '/' + friend_uid, relationship)
        self._set_db_data('relationships/' + friend_uid + \
                '/' + self.get_uid(), relationship)

    def add_endorsement(self, formdata):
        uid_to = formdata['uid_to']
        endorsement_text = formdata['endorsement_text']
        time = formdata['time']
        endorsement = {
            "text" : endorsement_text,
            "from" : self.get_uid(),
            "time" : time,
            "to"   : uid_to, # This is used to keep track of the
                             # final approver, aka which user can
                             # publish the endorsement
        }
        self._push_db_array('pending/' + uid_to, endorsement)

    def accept_pending(self, formdata):
        pending_uid = formdata['pending_uid']
        endorsement = self._pop_db_array('pending/' + self.get_uid() + '/' + pending_uid)
        if endorsement:
            uid_to = endorsement['to']
            # If you are the recipient, you can publish the endorsement
            if self.get_uid() == uid_to:
                del endorsement['to']
                self._push_db_array('endorsements/' + uid_to, endorsement)
            else:
                # otherwise, you need to push it to the recipient's 
                # queue for final acceptance
                self._push_db_array('pending/' + uid_to, endorsement)

    def amend_pending(self, formdata):
        pending_uid = formdata['pending_uid']
        updated_text = formdata['updated_text']
        endorsement = self._pop_db_array('pending/' + self.get_uid() + '/' + pending_uid)
        if endorsement:
            endorsement['text'] = updated_text
            next_uid = endorsement['from'] if endorsement['to'] == self.get_uid() else endorsement['to']
            self._push_db_array('pending/' + next_uid, endorsement)

    def reject_pending(self, formdata):
        pending_uid = formdata['pending_uid']
        self._pop_db_array('pending/' + self.get_uid() + '/' + pending_uid)
