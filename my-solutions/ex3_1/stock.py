import csv
import sys
from rich import print
sys.path.insert(0, '/Users/PI/code/python-mastery/my-solutions')


class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

    @staticmethod
    def read_portfolio(filename: str):
        with open(filename, 'r') as f:
            rows = csv.reader(f)
            headers = next(rows)
            coltypes = [str,int,float]
            portfolio = []
            for stock in rows:
                portfolio.append(Stock(**{name: cast(value) for name, cast, value in zip(headers, coltypes, stock)}))
            return portfolio


if __name__ == '__main__': 
    print(Stock.read_portfolio('../Data/portfolio.csv'))