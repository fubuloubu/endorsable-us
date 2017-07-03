#!/usr/bin/env python
from auto_user import AutoUser

class TrialUser(AutoUser):
    def __init__(self, name, email):
        AutoUser.__init__(self, name, email)
    
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
    
    def use_website(self, timeout=180, step=30):
        super().use_website(timeout=timeout, step=step)

def main(userfile, runtime, numthreads):
    
    from ast import literal_eval
    userlist = []
    with open(userfile, 'r') as f:
        for userdata in f.readlines():
            userlist.append(TrialUser(**literal_eval(userdata)))

    from multiprocessing.dummy import Pool as ThreadPool
    pool = ThreadPool(numthreads)
    pool.map(lambda u: u.use_website(timeout=runtime/60), userlist)
    pool.close() # Close the pool
    pool.join() # Wait for the trials to end

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run a simulation of N users given simple rules')
    parser.add_argument('userfile', type=str,
                                help='''File to obtain the userlist 
                                (collection of names and emails in csv format) from''')
    parser.add_argument('--runtime', metavar='T', type=int, default=3,
                                help='Time (in minutes) to run simulation for (default is 3 mins)')
    parser.add_argument('-t', '--numthreads', metavar='T', type=int, default=2,
                                help='Number of threads to use for simulation (default is 2 threads)')
    main(**vars(parser.parse_args()))
