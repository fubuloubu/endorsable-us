from auto_user import AutoUser

class Bot(AutoUser):
    # Overriden
    def pending_behavior(self, pending):
        # Default is to accept all
        self.accept_pending(pending)

    # Overriden
    def relationship_behavior(self, user):
        # Default is to send a new endorsement every time
        self.add_endorsement(user)

    # Overriden
    def unrelated_behavior(self, user):
        # Default is to befriend all people
        self.add_relationship(user)
