# readrides.py

import csv
from datetime import datetime
import tracemalloc
from collections import namedtuple

from attr import dataclass
from pydantic import BaseModel
from rich import print
import sys


def ride_record(ride):
    return {'route': ride[0], 'date': ride[1], 'daytype': ride[2], 'rides': ride[3]}


def store_as_dict(records: list[any]) -> any:

    return list(map(ride_record, records))


def store_as_dataclass(records: list[any]):

    @dataclass
    class RowDataclass(BaseModel):
        route: int
        date: datetime
        daytype: str
        rides: int

    return map(lambda ride: RowDataclass(ride[0], ride[1], ride[2], ride[3]), records)


def store_as_pydantic_objs(records: list[any]):

    class RowPydantic(BaseModel):
        route: int
        date: datetime
        daytype: str
        rides: int

    return map(lambda ride: RowPydantic(ride[0], ride[1], ride[2], ride[3]), records)


def store_as_objs(records: list[any]) -> any:

    class Row:
        def __init__(self, route, date, daytype, rides):
            self.route = route
            self.date = date
            self.daytype = daytype
            self.rides = rides

    return map(lambda ride: Row(ride[0], ride[1], ride[2], ride[3]), records)


def store_as_tuples(records: list[any]) -> any:
    return map(lambda ride: (ride[0], ride[1], ride[2], ride[3]), records)


def store_as_named_tuple(records: list[any]) -> list[any]:

    Row = namedtuple('Row', ['route', 'date', 'daytype', 'rides'])

    return map(
        lambda ride: Row(route=ride[0], date=ride[1],
                         daytype=ride[2], rides=ride[3]),
        records,
    )


def memory_status(type: str, m: map, last_memstatus: int) -> None:
    current, peak = tracemalloc.get_traced_memory()
    delta = current - last_memstatus
    MB = 1024 * 1024
    KB = 1024
    print(f"Memory Use of {type}: Current %dkb, Peak %dkb" %
          (delta / KB, peak / KB))
    # l = list(m)
    # list_size = sys.getsizeof(sum(o) for o in l)
    # print(f'Size of list: {list_size}')
    print(f'Current {current} Peak:{peak}')
    return current, peak


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

    start, _ = tracemalloc.get_traced_memory()
    l = store_as_dict(records)
    current, _ = memory_status('Dict', l, start)
    
    l = store_as_objs(records)
    current, _ = memory_status('Objs', l, current)

    l = store_as_named_tuple(records)
    current, _ = memory_status('Named tuples', l, current)

    l = store_as_tuples(records)
    current, _ = memory_status('Tuples', l, current)

    l = store_as_pydantic_objs(records)
    current, _ = memory_status('Pydantic Objs', l, current)

    l = store_as_dataclass(records)        
    current, _ = memory_status('Dataclass Objs', l, current)
