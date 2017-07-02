from basic_user import BasicUser
import polling

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
        error = self.register(registration_data)
        if error:
            self.login(self.login_data)
        self.uid = super().get_uid() # Store it so we don't have to constantly reference it
        print('({0}) Logged in'.format(self.get_uid()))

    def get_uid(self):
        return self.uid

    def __deinit__(self):
        self.logout()
    
    # Utility Methods (basically generate forms for base methods)
    def add_relationship(self, friend, rtype='friend'):
        formdata = {
            'friend_uid' : friend['uid'],
            'relationship' : rtype
        }
        print('({0}) Add {2} {1}'.format(self.get_uid(), friend['uid'], rtype))
        super().add_relationship(formdata)

    def add_endorsement(self, to, endorsement_text='Robots have nothing interesting to say'):
        formdata = {
            'uid_to' : to['uid'],
            'endorsement_text' : endorsement_text,
            'time' : 'now'
        }
        print('({0}) Add endr (to={1})'.format(self.get_uid(), to['uid']))
        super().add_endorsement(formdata)

    def accept_pending(self, pending):
        formdata = {
            'pending_uid' : pending['key'],
        }
        print('({0}) Accept endr (id={1})'.format(self.get_uid(), pending['key']))
        super().accept_pending(formdata)

    def amend_pending(self, pending_uid, updated_text='Yes we do!'):
        formdata = {
            'pending_uid' : pending['key'],
            'updated_text' : updated_text
        }
        print('({0}) Amend endr (id={1})'.format(self.get_uid(), pending['key']))
        super().amend_pending(formdata)

    def reject_pending(self, pending_uid):
        formdata = {
            'pending_uid' : pending['key'],
        }
        print('({0}) Reject endr (id={1})'.format(self.get_uid(), pending['key']))
        super().reject_pending(formdata)
    
    # Automated Methods
    def pending_behavior(self, pending):
        # Default is to accept all
        self.accept_pending(pending)

    def relationship_behavior(self, user):
        # Default is to send a new endorsement every time
        self.add_endorsement(user)

    def unrelated_behavior(self, user):
        # Default is to befriend all people
        self.add_relationship(user)

    def run_behavior(self):
        for p in self.get_pending_endorsements():
            self.pending_behavior(p)
        
        my_peeps = self.get_relationships()
        for u in my_peeps:
            self.relationship_behavior(u)
        
        my_peeps = [u['uid'] for u in my_peeps]
        other_peeps = [u for u in self.get_all_users() \
                if u['uid'] not in my_peeps and u['uid'] != self.get_uid()] 
        for u in other_peeps:
            self.unrelated_behavior(u)

        # Return true if there any reasons to exit polling
        return not self.authenticated()

    def use_website(self, **kwargs):
        # Poll the website for updates
        polling.poll(self.run_behavior, **kwargs)

if __name__ == '__main__':
    john = AutoUser()
    john.use_website(timeout=180, step=30)
