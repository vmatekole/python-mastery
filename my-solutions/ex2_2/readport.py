from rich import print

from collections import Counter, defaultdict

import csv

def read_portfolio(filename):
    portfolio = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            record = {
                'name' : row[0],
                'shares' : int(row[1]),
                'price' : float(row[2])
            }
            portfolio.append(record)
    return portfolio



if __name__ == '__main__':
    p = read_portfolio('../Data/portfolio.csv')
    print(p)


    totals = Counter()


    for s in p:
        totals[s['name']] += s['shares']

    more = Counter()

    more['IBM'] = 75
    more['AA'] = 100
    more['ACME'] = 20


    byname = defaultdict(list)

    for s in p:
        byname[s['name']].append(s)

    print(byname)

    # print(totals)
    # print(totals.most_common(2))
    # print(totals + more)

