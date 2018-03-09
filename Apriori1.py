import argparse
from itertools import chain, combinations

transactions = []
rules = []

def get_args():
    args = argparse.ArgumentParser()
    args.add_argument(
        '-f',
        dest='file',
        required=True
    )
    args.add_argument(
        '-s',
        dest='min_sup',
        type=float,
        required=True
    )
    args.add_argument(
        '-c',
        dest='min_conf',
        default=0.5,
        type=float
    )

    return args.parse_args()

def get_sup(i,n_transactions):
    sup = 0

    for x in transactions:
        flag = 1
        for y in i:
            if y:
                if y in x:
                    None
                else:
                    flag = 0
        if flag == 1:
            sup = sup + 1
    
    sup = sup/n_transactions

    return sup

def apriori(elem,n_transactions,min_conf,min_sup):
    
    list1 = list(chain(*[combinations(elem,i+1) for i in range(len(elem))]))
    list2 = []
    
    for i in list1:
        if get_sup(i,n_transactions) >= min_sup:
            list2.append(i) 

    # for x in list1:
    #     print(x,get_sup(x,n_transactions))

    #print (list2)

    for x in list2:
        for y in list2:
            flag = 1

            for a in x:
                if a in y:
                    flag = 0

            if x != y and flag == 1:
                s = get_sup(x+y, n_transactions)
                # print (x+y,s)
                if s >= min_sup:    
                    rules.append(create_rule(x, y, 0, s))        

    
def print_list(rules,file):
    rules.sort(key=lambda x: (len(x.s1 + x.s2),x.conf,x.sup),  reverse=True)

    print('Mined file {} and found a total of {} association rules.'.format(file,len(rules)))
    print('\nRule\t\t\tConfidence\tSupport')
        
    for r in rules:
        print('{} \t==> {} \t{:.3} \t\t{:.3}'.format(set(r.s1),set(r.s2),r.conf,r.sup))

def get_conf(rules,min_conf):
    conf = 0
    tot = 0
    for r in rules:
        conf = 0
        tot = 0
        for x in transactions:
            flag1 = 1
            flag2 = 1
            for i in r.s1:
                if i not in x:
                    flag1 = 0
            if flag1 == 1:
                tot = tot + 1
                for j in r.s2:
                    if j not in x:
                        flag2 = 0
                if flag2 == 1:
                    conf = conf + 1
        r.conf = conf/tot
    
    rules_final = []

    for r in rules:
        if r.conf >= min_conf:
            rules_final.append(r)

    return rules_final


def create_rule(s1, s2, conf, sup):
    return Rule(s1, s2, conf, sup)

class Rule:
    def __init__( self, s1, s2, conf, sup ):
        self.s1 = s1
        self.s2 = s2
        self.conf = conf
        self.sup = sup

def main():
    arguments = get_args()
    s = set()
    #print(arguments.file,arguments.min_conf,arguments.min_sup)

    f1 = open(arguments.file)
    n_transactions = 0

    for row in f1:
        transactions.append(list(map(int,row.split())))
        n_transactions = n_transactions + 1

    for x in transactions:
        for y in x:
            s.add(y)
        
    elements = list(s)

    apriori(elements,n_transactions,arguments.min_conf,arguments.min_sup)
    rules_final = get_conf(rules,arguments.min_conf)
    print_list(rules_final,arguments.file)

    #print (elem)
    #print(s,elements)
    #print(transactions)

if __name__ == '__main__':
    main()