from database import Database

class BasicUser(Database):
    def __init__(self):
        Database.__init__(self)
    
    # Getters
    def get_user_relationships(self, user_uid):
        return self._get_db_array('relationships/' + user_uid, valname='type', keyname='uid')

    def get_relationships(self):
        return self.get_user_relationships(self.get_uid())

    def is_friend(self, user_uid):
        return user_uid in [r['uid'] for r in self.get_relationships()]

    def get_pending_endorsements(self):
        return self._get_db_array('pending/' + self.get_uid())
    
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
            del endorsement['to']
            self._push_db_array('endorsements/' + uid_to, endorsement)

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
