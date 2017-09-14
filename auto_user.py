from basic_user import BasicUser
from time import sleep

class AutoUser(BasicUser):
    def __init__(self, name='John Smith', email='johnsmith@johnsonsjohnsons.net'):
        BasicUser.__init__(self)
        registration_data = {
            'fullname' : name,
            'email' : email,
            'password' : 'password'
        }
        self.login_data = {
            'email' : email,
            'password' : 'password'
        }
        error = self.login(self.login_data)
        if error:
            self.register(registration_data)
        self.uid = self.get_uid() # Store it so we don't have to constantly reference it
        # Some reason this fails when registering
        print('({0}) Logged in'.format(self.get_uid()))

    def __deinit__(self):
        self.logout()
    
    # Utility Methods (basically generate forms for base methods)
    def add_relationship(self, friend, rtype='friend'):
        formdata = {
            'friend_uid' : friend['uid'],
            'relationship' : rtype
        }
        print('({0}) Add {2} {1}'.format(self.uid, friend['uid'], rtype))
        super().add_relationship(formdata)

    def add_endorsement(self, to, endorsement_text='Robots have nothing interesting to say'):
        formdata = {
            'uid_to' : to['uid'],
            'endorsement_text' : endorsement_text,
            'time' : 'now'
        }
        print('({0}) Add endr (to={1})'.format(self.uid, to['uid']))
        super().add_endorsement(formdata)

    def accept_pending(self, pending):
        formdata = {
            'pending_uid' : pending['key'],
        }
        print('({0}) Accept endr (id={1})'.format(self.uid, pending['key']))
        super().accept_pending(formdata)

    def amend_pending(self, pending_uid, updated_text='Yes we do!'):
        formdata = {
            'pending_uid' : pending['key'],
            'updated_text' : updated_text
        }
        print('({0}) Amend endr (id={1})'.format(self.uid, pending['key']))
        super().amend_pending(formdata)

    def reject_pending(self, pending_uid):
        formdata = {
            'pending_uid' : pending['key'],
        }
        print('({0}) Reject endr (id={1})'.format(self.uid, pending['key']))
        super().reject_pending(formdata)
    
    # Automated Methods
    def pending_behavior(self, pending):
        print('({0}) Doing nothing in response to pending endorsement {1}'.
                format(self.uid, pending['key']))
        # Default is to do nothing
        pass

    def relationship_behavior(self, user):
        print('({0}) Doing nothing for my friend {1}'.format(self.uid, user['uid']))
        # Default is to do nothing
        pass

    def unrelated_behavior(self, user):
        print("({0}) Doing nothing for unknown user {1}".format(self.uid, user['uid']))
        # Default is to do nothing
        pass

    def run_behavior(self, pausetime=1):
        for p in self.get_pending_endorsements():
            self.pending_behavior(p)
            sleep(pausetime) # Added so it doesn't make too many requests at a time
        
        my_peeps = self.get_relationships()
        for u in my_peeps:
            self.relationship_behavior(u)
            sleep(pausetime) # Added so it doesn't make too many requests at a time
        
        my_peeps = [u['uid'] for u in my_peeps]
        other_peeps = [u for u in self.get_all_users() \
                if u['uid'] not in my_peeps and u['uid'] != self.uid] 
        for u in other_peeps:
            self.unrelated_behavior(u)
            sleep(pausetime) # Added so it doesn't make too many requests at a time

        # Return true if there any reasons to exit polling
        return not self.authenticated()

    def use_website(self, timeout=180, step=30):
        # Poll the website for updates
        while timeout > 0:
            self.run_behavior()
            sleep(step)
            timeout -= step
        #polling.poll(self.run_behavior, **kwargs)
