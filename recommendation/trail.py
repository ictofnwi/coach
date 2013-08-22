import sys
from collections import defaultdict

# For debug purposes
from apriori import display_dict

def score(D, gamma = 0.9):
    '''Assigns a score to each consequent-antecedent-pair in the transactions.
    The gamma operator discounts items that lie further apart.

    D:      Dataset containing transactions.
    gamma:  Discount factor

    NOTE: This method assumes that the items within the transactions are sorted.
    '''

    score_dict = dict() # Keeps track of the discounted counts
    multi_dict = dict() # Keeps track of maximal discounted sum (in case of multiple occurence)

    def update(trail, cons):
        '''Updates the scores and counts for the given consequent according to
        the given (partial) trail.
        '''
        count_dict = defaultdict(int)

        if cons not in score_dict:
            score_dict[cons] = defaultdict(float)
            multi_dict[cons] = defaultdict(float)

        for i, item in enumerate(trail):
            score_dict[cons][item] += gamma ** i
            multi_dict[cons][item] += gamma ** count_dict[item]
            count_dict[item] += 1

    for trail in D.itervalues():
        trail_list = list(reversed(trail))
        for i, item in enumerate(trail_list):
            update(trail_list[i+1:], item)

    return score_dict, multi_dict

def generate_rules(D, gamma, minsupp, minconf, verbose = False):
    '''Generates rules according to the scores of the items.

    D:          Dataset containing transactions.
    gamma:      Discount factor.
    minsupp:    Support threshold.
    minconf:    Confidence threshold.
    '''
    score_dict, multi_dict = score(D, gamma)

    rules = set()

    for cons in score_dict:
        for ante in score_dict[cons]:
            supp = float(score_dict[cons][ante])
            conf = supp / float(multi_dict[cons][ante])
        
            if supp >= minsupp and conf >= minconf:
                rules.add((ante, cons, conf, supp))

    return rules

if __name__ == '__main__':
    # Test Data
    D = {100: (1,1,4,5,4),
         200: (1,2,4),
         300: (1,2,3,5),
         400: (2,5),
         500: (1,2,2,2,4,5,3),
         600: (1,3,2,4,5),
         700: (1,2,5,4)}

    gamma = float(sys.argv[1])
    minsupp = float(sys.argv[2])
    minconf = float(sys.argv[3])

    rules = generate_rules(D, gamma, minsupp, minconf)

    for rule in rules:
        print '{0} --> {1} | {2} | {3}'.format(rule[0],rule[1],rule[2],rule[3])
