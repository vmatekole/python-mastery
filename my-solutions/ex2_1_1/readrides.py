# readrides.py

from collections import namedtuple
from rich import print
import csv
import tracemalloc


def ride_record(ride): return {
    'route': ride[0],
    'date': ride[1],
    'daytype': ride[2],
    'rides': ride[3]
}


def store_as_dict(records: list[any]) -> any:

    return list(map(ride_record, records))


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

    return map(lambda ride: Row(route=ride[0], date=ride[1], daytype=ride[2], rides=ride[3]), records)


def memory_status(type: str, last_memstatus: int) -> None:
    current, peak = tracemalloc.get_traced_memory()
    delta = current - last_memstatus
    MB = 1024 * 1024
    KB = 1024
    print(f'Memory Use of {type}: Current %dkb, Peak %dkb' %
          (delta / KB, peak / KB))
    return current, peak


def read_rides(filename: str) -> list[any]:
    '''
    Read the bus ride data as a list of tuples
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            records.append((route, date, daytype, rides))

        last_memstatus, peak = tracemalloc.get_traced_memory()
        store_as_dict(records)
        last_memstatus, peak = memory_status('Dict', last_memstatus)
        store_as_objs(records)
        last_memstatus, peak = memory_status('Objs', last_memstatus)
        store_as_named_tuple(records)
        last_memstatus, peak = memory_status('Named tuples', last_memstatus)
        store_as_tuples(records)
        last_memstatus, peak = memory_status('Tuples', last_memstatus)


if __name__ == '__main__':
    import tracemalloc
    tracemalloc.start()
    read_rides('../Data/ctabus.csv')
