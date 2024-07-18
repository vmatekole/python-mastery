
from pprint import pprint

from rich import print

import csv


def squares(nums):
    for x in nums:
        yield x*x

if __name__ == '__main__':
    with open('../Data/portfolio.csv', 'r') as f:
        rows = csv.reader(f)
        headers = next(rows)

        # pprint(dict(zip(headers,rows)))

        for r in rows:
            print(dict(zip(headers,r)))
        
        nums = [n for n in range(1,10)]
        literal_squares = (n**2 for n in nums)
        squares_list = [n**2 for n in nums]
        
        # print(list(literal_squares)[1])
        # print(squares_list)

        # for n in squares(nums):
        #     print(n)

        print(max(squares(nums)))

        print(any(n for n in squares(nums) if n == 81))

    

