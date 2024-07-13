# readrides.py

import csv
from collections import defaultdict
from typing import Counter
import datetime
from rich import print

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
            date: datetime.date = datetime.datetime.strptime(row[1], '%m/%d/%Y').date()
            daytype = row[2]
            rides = int(row[3])
            records.append((route, date, daytype, rides))
    return records

def total_rides_by_bus_date(records, route, date):
    return len([ride for ride in records if ride.route == route and ride.date == date])

def total_rides_by_bus_year(records, route, year):
    return len([ride for ride in records if ride.route == route and ride.date.year == year])


if __name__ == '__main__':
    records = read_rides('../Data/ctabus.csv')
    rides = store_as_slots(records)

    byroute = defaultdict(list) 

    route_totals: Counter = Counter()
    for r in rides:
        route_totals[r.route] += 1

    for y in range(2001,2012):
        for r in route_totals.keys():
            byroute[r].append({'num_rides': total_rides_by_bus_year(rides,r,y), 'year': y})
    
    ten_yr_delta = Counter()

    for route in route_totals.keys():
        num_rides = lambda x: x['num_rides']
        ten_yr_delta[route] = max(byroute[route], key=num_rides)['num_rides'] - min(byroute[route], key=num_rides)['num_rides']

    yearly_totals = []    
    for ride in rides:
        yearly_totals.append({'route': ride.route, 'total': route_totals[ride.route]})

    print(route_totals)
    print(f'Number of routes: {len(route_totals)}')
    print(f'Number of rides on 22 bus on 02/02/2001: {total_rides_by_bus_date(rides,'22',datetime.date(2001,2,2))}')
    print(f'Number of rides on each bus route: {route_totals}')
    print(f'Five routes with biggest ten yr increase: {ten_yr_delta.most_common(5)}')
