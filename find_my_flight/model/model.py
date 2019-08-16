import datetime as dt


class Point:
    def __init__(self, country: str, city: str):
        self.country = country
        self.city = city


class Approximate:
    def __init__(self, value, plus_minus):
        self.value = value
        self.plus_minus = plus_minus

    def astuple(self):
        return self.value, self.plus_minus


def add_month(d: dt.date) -> dt.date:
    return dt.date(d.year + int(d.month / 12), (d.month % 12) + 1, d.day)


class PartialDate:
    def __init__(self, year, month):
        self.month = month
        self.year = year

    @staticmethod
    def from_date(date: dt.date):
        return PartialDate(date.year, date.month)

    def get_next_month(self):
        first_day = dt.date(self.year, self.month, 1)
        next_month = add_month(first_day)
        return PartialDate(next_month.year, next_month.month)

    def __lt__(self, other):
        return self.year < other.year or (self.year <= other.year and self.month < other.month)

    def __le__(self, other):
        return self < other or (self == other)

    def __eq__(self, other):
        return self.year == other.year and self.month == other.month

    def __str__(self):
        return f'{self.year}-{self.month:02d}'


class ApproximateFlightFilter:
    def __init__(
            self,
            origin: Point, destination: Point,
            outbound_date_not_earlier: dt.datetime,
            inbound_date_not_later: dt.datetime,
            approx_trip_length_days: int,
            plus_minus_days: int):
        self.origin = origin
        self.destination = destination
        self.outbound_date_not_earlier = outbound_date_not_earlier
        self.inbound_date_not_later = inbound_date_not_later
        self.approx_trip_length_days = approx_trip_length_days
        self.plus_minus_days = plus_minus_days
