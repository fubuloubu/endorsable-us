from basic_user import BasicUser

class AutoUser(BasicUser):
    def __init__(self, name, email):
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

    def __deinit__(self):
        self.logout()
    
    # Utility Methods (basically generate forms for base methods)
    def add_relationship(self, friend_uid):
        formdata = {
            'friend_uid' : friend_uid,
            'relationship' : 'friend'
        }
        super().add_relationship(formdata)

    def add_endorsement(self, uid_to):
        endorsement_text = 'Robots have nothing interesting to say'
        formdata = {
            'uid_to' : uid_to,
            'endorsement_text' : endorsement_text,
            'time' : 'now'
        }
        super().add_endorsement(formdata)

    def accept_pending(self, pending_uid):
        formdata = {
            'pending_uid' : pending_uid,
        }
        super().accept_pending(formdata)

    def amend_pending(self, pending_uid):
        updated_text = 'Yes we do!'
        formdata = {
            'pending_uid' : pending_uid,
            'updated_text' : updated_text
        }
        super().amend_pending(formdata)

    def reject_pending(self, pending_uid):
        formdata = {
            'pending_uid' : pending_uid,
        }
        super().reject_pending(formdata)
    
    # Automated Methods

if __name__ == '__main__':
    john = AutoUser('John Smith', 'johnsmith@johnsonsjohnsons.net')
    bobs_uid = 'dZeZA8S24cWuziaBagktgeWxbjh1'
    john.add_relationship(bobs_uid)
    john.add_endorsement(bobs_uid)
