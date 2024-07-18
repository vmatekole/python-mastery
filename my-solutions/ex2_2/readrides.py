# readrides.py

from calendar import month
import csv
from collections import defaultdict
import itertools
import time
from typing import Counter
import datetime
from rich import print


def store_as_slots(records: list[any]):
    class RowSlot:
        # __slots__ = ['route', 'date', 'daytype', 'rides']
        def __init__(self, route, date, daytype, rides):
            self.route = route
            self.date = date
            self.daytype = daytype
            self.rides = rides

    return [RowSlot(route=ride[0], date=ride[1][0], daytype=ride[1][1], rides=ride[1][2]) for ride in records]


def read_rides(filename: str):
    """
    Read the bus ride data as a list of tuples
    """
    records = defaultdict(list)
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        # t = list(itertools.islice(rows, 10000))
        for row in rows:
            route = row[0]
            date: datetime.date = datetime.datetime.strptime(
                row[1], '%m/%d/%Y').date().strftime('%d/%m/%Y')
            daytype = row[2]
            rides = int(row[3])
            if not records[route]:
                records[route] =  {}
                records[route]['monthly_trips'] =  {}
            records[route]['monthly_trips'][date] = {'daytype': daytype, 'rides': rides}
    return records

if __name__ == '__main__':    
    trips = read_rides('../Data/ctabus.csv')

    annual_trips = {}
    total_trips_per_route = Counter()

    for route in trips.keys():
        for date in trips[route]['monthly_trips'].keys(): 
            year =  date[-4:] # 01/01/2001 - parse the year
            
            if route not in annual_trips:
                annual_trips[route] = {} 
            if year not in annual_trips[route]:
                annual_trips[route][str(year)] = 0

            annual_trips[route][str(year)] = sum(trips[route]['monthly_trips'][date]['rides']  for date in trips[route]['monthly_trips'].keys() if date.endswith(str(year)))         
        total_trips_per_route[route] = sum(annual_trips[route].values())
        print(f'Processed {len(total_trips_per_route)} of {len(trips.keys())} routes...', end='\r')
            

    ten_yr_delta = Counter()
    
    for route in annual_trips:
        trips_2001_2010 = [annual_trips[route][year] for year in annual_trips[route].keys() if int(year) > 2001 and int(year) < 2010]
        if trips_2001_2010:
            max_num_trips = max(trips_2001_2010) 
            min_num_trips = min(trips_2001_2010)

        ten_yr_delta[route] = f'Increase in trips between 2001-2010: {max_num_trips-min_num_trips}. Percentage increase: {((min_num_trips/max_num_trips)*100):.2f}%'

    print(f'Number of routes: {len(trips.keys())}')
    print(f'Number of rides on 22 bus on 02/02/2011: {trips["22"]["monthly_trips"]["02/02/2011"]}')
    print(f'Number of rides on each bus route: {total_trips_per_route}')
    print(f'Five routes with biggest ten yr increase: {ten_yr_delta.most_common(5)}')