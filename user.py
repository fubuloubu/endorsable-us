from database import Database

class User(Database):
    def __init__(self):
        Database.__init__(self)

    def get_user_data(self, user_uid):
        return self._get_db_data('users/' + user_uid)

    def get_user_relationships(self):
        return self._get_db_data('relationships/' + self.get_uid())

    def get_endorsements_by_uid(self, user_uid):
        return self._get_db_data('endorsements/' + user_uid)

    def get_all_endorsements(self):
        endorsements = []
        friends = self.get_user_relationships()
        if friends: # User has friends
            for uid in friends.keys():
                endorsements.extend(self.get_endorsements_by_uid(uid))
        return endorsements

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
        endorsement = self._pop_db_data('pending/' + self.get_uid() + '/' + pending_uid)
        uid_to = endorsement['to']
        del endorsement['to']
        self._push_db_data('endorsements/' + uid_to, endorsement)

    def amend_pending(self, pending_uid, updated_text):
        endorsement = self._pop_db_data('pending/' + self.get_uid() + '/' + pending_uid)
        endorsement['text'] = updated_text
        next_uid = endorsement['from'] if endorsement['to'] == self.get_uid() else endorsement['to']
        self._push_db_data('pending/' + next_uid, endorsement)

    def reject_pending(self, pending_uid):
        self._pop_db_data('pending/' + self.get_uid() + '/' + pending_uid)
