# readrides.py

import csv
from datetime import datetime, date
import tracemalloc
from collections import namedtuple

from dataclasses import dataclass
from pydantic import BaseModel, field_validator
from rich import print
import sys




def ride_record(ride):
    return {'route': ride[0], 'date': ride[1], 'daytype': ride[2], 'rides': ride[3]}


def store_as_dict(records: list[any]) -> any:

    return [ride_record(ride) for ride in records]


def store_as_dataclass(records: list[any]):

    @dataclass
    class RowDataclass():
        route: int
        date: datetime
        daytype: str
        rides: int

    return [RowDataclass(ride[0], ride[1], ride[2], ride[3]) for ride in records]


def store_as_pydantic_objs(records: list[any]):

    class RowPydantic(BaseModel):
        route: str
        date: date
        daytype: str
        rides: int

    
        @field_validator('date', mode='before')
        def parse_date(cls, value):
            if isinstance(value, date):
                return value
            try:
                # Assuming the date format is DD/MM/YYYY
                d = datetime.strptime(value, '%m/%d/%Y').date()


                return d
            except ValueError:
                raise ValueError("Incorrect date format, should be DD/MM/YYYY")
    

    return [RowPydantic(route=ride[0], date=ride[1], daytype=ride[2], rides=ride[3]) for ride in records]


def store_as_objs(records: list[any]) -> any:

    class Row:
        def __init__(self, route, date, daytype, rides):
            self.route = route
            self.date = date
            self.daytype = daytype
            self.rides = rides

    return [Row(ride[0], ride[1], ride[2], ride[3]) for ride in records]


def store_as_tuples(records: list[any]) -> any:
    return map(lambda ride: (ride[0], ride[1], ride[2], ride[3]), records)


def store_as_named_tuple(records: list[any]) -> list[any]:

    Row = namedtuple('Row', ['route', 'date', 'daytype', 'rides'])

    return [Row(route=ride[0], date=ride[1], daytype=ride[2], rides=ride[3]) for ride in records]


def memory_status(type: str, l: list) -> None:
    current, peak = tracemalloc.get_traced_memory()
    MB = 1024 * 1024
    print(f"Memory Use of {type}: Current %dmb, Peak %dmb" %
          (current / MB, peak / MB))

    t =  sum([sys.getsizeof(t) / MB for t in l])
    list_size = t
    print(f'Size of list: {list_size}mb')
    print(f'Current {current} Peak:{peak}')


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
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            records.append((route, date, daytype, rides))
    return records

if __name__ == '__main__':
    import tracemalloc

    tracemalloc.start()
    records = read_rides('../Data/ctabus.csv')

    l = store_as_dict(records)
    memory_status('Dict', l)
    
    l = store_as_objs(records)
    memory_status('Objs', l)

    l = store_as_named_tuple(records)
    memory_status('Named tuples', l)

    l = store_as_tuples(records)
    memory_status('Tuples', l)

    l = store_as_pydantic_objs(records)
    memory_status('Pydantic Objs', l)

    l = store_as_dataclass(records)        
    memory_status('Dataclass Objs', l)

    # snapshot = tracemalloc.take_snapshot()

    # for s in snapshot.statistics('lineno'):
    #     print(s)



