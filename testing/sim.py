# Percentage of week on platform (aiming for 2% = 48 mins)
def usage_model(guilt=0.1, enjoyment=0.2, usefulness=0.05):
    return enjoyment**(guilt*usefulness)

def reputation_model(reputation, rate_fun):
    return reputation + rate_fun(reputation)

def growth_model(num_users, rate_fun):
    return num_users + rate_fun(num_users)

def main(initial_coins, initial_price, reputation_rate, growth_rate):
    print(initial_coins, initial_price, reputation_rate, growth_rate)

if __name__ == '__main__':
    import argparse
    import ast
    # Helper class for lambdas
    class LambdaAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            print(parser, namespace, values, option_string)
            values = ast.literal_eval(values)
            setattr(namespace, self.dest, values)

    parser = argparse.ArgumentParser(description='Run coin forecast for user growth rate and usage')
    # System properties
    parser.add_argument('-c', '--initial-coins', type=int, default=10**9, 
            help='The total number of starting coins')
    parser.add_argument('-p', '--initial-price', type=float, default=20.0, 
            help='Price (in USD) of initial coin')
    parser.add_argument('-r', '--reputation-rate', action=LambdaAction, default=lambda r: r, 
            help='User reputation growth rate r_N = r_N-1 + f(r_N-1), time in weeks')
    # Adoption properties
    parser.add_argument('-g', '--growth-rate', action=LambdaAction, default=lambda x: x, 
            help='User growth rate x_N = X_N-1 + f(x_N-1), time in weeks')
    main(**vars(parser.parse_args()))
