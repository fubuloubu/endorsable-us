from basic_user import BasicUser

class WebUser(BasicUser):
    def __init__(self):
        BasicUser.__init__(self)
    
    # Getters
    def get_user_name(self, user_uid):
        return self._get_db_data('users/' + user_uid + '/name')
    
    def get_name(self):
        return self.get_user_name(self.get_uid())

    def get_user_data(self, user_uid):
        userdata = self._get_db_data('users/' + user_uid)
        # Don't give out contact information
        if self.get_uid() != user_uid:
            del userdata['email']
        userdata['uid'] = user_uid
        friends = self.get_user_relationships(user_uid)
        if friends: # User has friends
            #Add name from key, change value to type
            for friend in friends:
                friend['name'] = self.get_user_name(friend['uid'])
            userdata['relationships'] = friends
        return userdata
    
    def get_data(self):
        return self.get_user_data(self.get_uid())

    def get_user_endorsements(self, user_uid):
        endorsements = self._get_db_array('endorsements/' + user_uid)
        user_name = self.get_user_name(user_uid)
        for endr in endorsements:
            endr['toname'] = user_name
            endr['fromname'] = self.get_user_name(endr['from'])
        return endorsements

    def get_endorsements(self):
        return self.get_user_endorsements(self.get_uid())

    def get_timeline_endorsements(self):
        # User + Friends
        endorsements = []
        endorsements.extend(self.get_endorsements())
        friends = self.get_relationships()
        if friends: # User has friends
            for friend in friends:
                endorsements.extend(self.get_user_endorsements(friend['uid']))
        return endorsements

