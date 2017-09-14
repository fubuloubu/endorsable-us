#!/usr/bin/env python
from auto_user import AutoUser

def main(userclass, userfile, runtime, numthreads):
    
    from ast import literal_eval
    userlist = []
    with open(userfile, 'r') as f:
        for userdata in f.readlines():
            userlist.append(userclass(**literal_eval(userdata)))

    from multiprocessing.dummy import Pool as ThreadPool
    pool = ThreadPool(numthreads)
    pool.map(lambda u: u.use_website(timeout=runtime/60), userlist)
    pool.close() # Close the pool
    pool.join() # Wait for the trials to end

if __name__ == '__main__':
    import argparse
    import ast
    
    class GetClass(argparse.Action):
        def __call__(self, parser, namespace, fname, option_string=None):
            with open(fname, 'r') as f:
                prog = ast.parse(f.read())
            classes = [node.name for node in ast.walk(prog) if isinstance(node, ast.ClassDef)]
            assert len(classes) == 1
            exec('from {} import {}'.format(fname.strip('.py'), classes[0]))
            setattr(namespace, self.dest, eval(classes[0]))

    parser = argparse.ArgumentParser(description='Run a simulation of N users given simple rules')
    parser.add_argument('-u', '--userclass', action=GetClass, default=AutoUser,
                                help="Python module to obtain simulated user's class from")
    parser.add_argument('userfile', type=str,
                                help='''File to obtain the userlist 
                                (collection of names and emails in csv format) from''')
    parser.add_argument('--runtime', metavar='T', type=int, default=3,
                                help='Time (in minutes) to run simulation for (default is 3 mins)')
    parser.add_argument('-t', '--numthreads', metavar='T', type=int, default=2,
                                help='Number of threads to use for simulation (default is 2 threads)')
    main(**vars(parser.parse_args()))
