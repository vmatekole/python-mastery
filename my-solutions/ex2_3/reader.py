
import tracemalloc

from readrides import read_rides, store_as_dict

from rich import print

import csv


def squares(nums):
    for x in nums:
        yield x*x


if __name__ == '__main__':
    with open('../Data/portfolio.csv', 'r') as f:
        rows = csv.reader(f)
        headers = next(rows)

        print(dict(zip(headers, rows)))

        for r in rows:
            print(dict(zip(headers, r)))

        nums = [n for n in range(1, 10)]
        literal_squares = (n**2 for n in nums)
        squares_list = [n**2 for n in nums]

        print(list(literal_squares)[1])
        print(squares_list)

        for n in squares(nums):
            print(n)

        print(max(squares(nums)))

        print(any(n for n in squares(nums) if n == 81))

        # Memory assessment
        tracemalloc.start()
        records = read_rides('../Data/ctabus.csv')
        l = store_as_dict(records)
        rt22 = [row for row in l if row['route'] == '22']
        max(rt22, key=lambda r: r['rides'])
        mem_usage, peak = tracemalloc.get_traced_memory()        
        print(f'Mem usage as a list {(mem_usage / (1024 * 1024)):.10f} mb Peak:{peak}')

        rt22 = (row for row in l if row['route'] == '22')
        max(rt22, key=lambda r: r['rides'])


        mem_usage, peak = tracemalloc.get_traced_memory()        
        print(f'Mem usage as a list {(mem_usage / (1024 * 1024)):.10f} mb Peak: {peak}')


