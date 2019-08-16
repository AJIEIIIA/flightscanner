import datetime as dt

from find_my_flight.model.model import PartialDate


def get_possible_partial_dates(earliest: dt.date, latest: dt.date, length_days: int, error_days: int):
    min_length = length_days - error_days
    start = earliest
    end = earliest + dt.timedelta(days=min_length)

    results = []
    while end <= latest:
        interval = (PartialDate.from_date(start), PartialDate.from_date(end))
        if len(results) == 0 or results[-1] != interval:
            results.append(interval)

        start = start + dt.timedelta(days=1)
        end = start + dt.timedelta(days=min_length)

    return results


def left_join_flights(t1, t2, constraint):
    results = []
    for flight in t1:
        joined = list(filter(lambda x: constraint(flight, x), t2))
        results.append((flight, joined))
    return results
