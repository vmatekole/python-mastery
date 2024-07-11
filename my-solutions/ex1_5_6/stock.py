import sys

sys.path.insert(0, '/Users/PI/code/python-mastery/my-solutions')
from ex1_3_4 import pcost


class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price
