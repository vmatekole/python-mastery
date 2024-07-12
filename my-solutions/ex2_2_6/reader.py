
from rich import print

import csv

def read_portfolio():

    with open('../Data/portfolio.csv', 'r') as f:
        rows = csv.reader(f)
        headers = next(rows) 
        return headers, [(row[0], row[1], row[2]) for row in rows]

if __name__ == '__main__':
    headers, portfolio = read_portfolio()
    coltypes = [str,int,float]
    # print(portfolio)
    # print(portfolio[0][1][1] * 3)
    # l = [[1]] * 3
    # print(hex(id(l[0])))
    # print(id(l[1]))
    # print(id(l))    

    typed_portfolio = []
    
    for row in portfolio:
        typed_portfolio.append({name:cast(val) for name, cast, val in zip(headers, coltypes, row)})

    print(typed_portfolio)
        