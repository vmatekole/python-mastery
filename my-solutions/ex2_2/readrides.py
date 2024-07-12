# readrides.py

import csv
import tracemalloc
from typing import Counter
import datetime
from rich import print
import sys

def store_as_slots(records: list[any]):
    class RowSlot:
        __slots__ = ['route', 'date', 'daytype', 'rides']
        def __init__(self, route, date, daytype, rides):
            self.route = route
            self.date = date
            self.daytype = daytype
            self.rides = rides
    
    return [RowSlot(route=ride[0],date=ride[1], daytype=ride[2], rides=ride[3]) for ride in records]

def read_rides(filename: str) -> list[any]:
    """
    Read the bus ride data as a list of tuples
    """
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = datetime.datetime.strptime(row[1], '%m/%d/%Y').date()
            daytype = row[2]
            rides = int(row[3])
            records.append((route, date, daytype, rides))
    return records

def total_rides_by_bus_date(records, route, date):
    return len([ride for ride in records if ride.route == route and ride.date == date])


if __name__ == '__main__':
    records = read_rides('../Data/ctabus.csv')
    l = store_as_slots(records)

    totals = Counter()
    print(l[0].date)
    for t in l:
        totals[t.route] += 1

    print(f'Number of routes: {len(totals)}')
    print(f'Number of rides on 22 bus on 02/02/2001: {total_rides_by_bus_date(l,'22',datetime.date(2001,2,2))}')
    print(f'Number of rides on each bus route: {totals}')
