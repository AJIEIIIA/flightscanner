import datetime as dt


def get_flight_dates(flight):
    inbound_date = dt.datetime.strptime(flight['InboundLeg']['DepartureDate'], '%Y-%m-%dT%H:%M:%S')
    outbound_date = dt.datetime.strptime(flight['OutboundLeg']['DepartureDate'], '%Y-%m-%dT%H:%M:%S')
    return outbound_date, inbound_date


def get_trip_length(quote):
    outbound_date, inbound_date = get_flight_dates(quote)
    return (inbound_date - outbound_date).days


class FlightConstraint:
    def __call__(self, flight: dict, *args, **kwargs) -> bool:
        pass


class WrappedConstraint(FlightConstraint):
    def __init__(self, constraints: list = None):
        self.constraints = constraints or []

    def add(self, c: FlightConstraint):
        self.constraints.append(c)

    def __call__(self, flight: dict, *args, **kwargs) -> bool:
        return all([x(flight, *args, **kwargs) for x in self.constraints])


class FlightIndicativeLengthConstraint(FlightConstraint):
    def __init__(self, indicative_length_days, plus_minus_days):
        self._indicative_length_days = indicative_length_days
        self._plus_minus_days = plus_minus_days
        self._min_length = indicative_length_days - plus_minus_days
        self._max_length = indicative_length_days + plus_minus_days

    def __call__(self, flight: dict, *args, **kwargs) -> bool:
        length = get_trip_length(flight)
        if self._min_length <= length <= self._max_length:
            return True
        return False


class FlightFitsInDatesConstraint(FlightConstraint):
    def __init__(self, t0: dt.datetime, t1: dt.datetime, slack_days: int = 0):
        self.t0 = t0
        self.t1 = t1
        self.slack = dt.timedelta(days=slack_days)

    def __call__(self, flight: dict, *args, **kwargs) -> bool:
        outbound_date, inbound_date = get_flight_dates(flight)
        return outbound_date > self.t0 + self.slack and inbound_date < self.t1 - self.slack


class FlightExclusionDatesConstraint(FlightConstraint):
    def __init__(self, dates: list):
        self.dates = dates

    def __call__(self, flight: dict, *args, **kwargs):
        outbound_date, inbound_date = get_flight_dates(flight)
        return all(map(lambda x: not outbound_date < x < inbound_date, self.dates))


class InnerFlightConstraint(FlightFitsInDatesConstraint):
    def __init__(self, main_flight: dict, slack_days: int):
        self.slack_days = slack_days
        self.main_flight = main_flight
        outbound_date, inbound_date = get_flight_dates(main_flight)
        super().__init__(outbound_date, inbound_date, slack_days)

    def __call__(self, flight, *args, **kwargs):
        return super().__call__(flight, args, kwargs)
