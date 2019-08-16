import find_my_flight.model.flight_constraint as fc
import find_my_flight.services.utils as utils
from find_my_flight.conn.sky_scanner_api import SkyScannerApiInterface, ListOfDict
from find_my_flight.model.model import ApproximateFlightFilter


def find_in_countries(countries: ListOfDict, target_name: str) -> ListOfDict:
    return [x for x in countries if x['Name'] == target_name]


def get_all_airports_place(conn: SkyScannerApiInterface, city, country, user_country=None):
    if user_country is None:
        user_country = country
    places = conn.get_places(user_country['Code'], city)
    all_airports_place = [x for x in places if x['CountryName'] == country['Name']][0]
    return all_airports_place


class FlightSearchEngine:
    def __init__(self, conn: SkyScannerApiInterface, user_country_name: str):
        self._conn = conn
        self._countries = conn.get_countries()
        self._user_country = find_in_countries(self._countries, user_country_name)[0]

    def search_flights_with_filter(self, flight_filter: ApproximateFlightFilter):
        origin_country = find_in_countries(self._countries, flight_filter.origin.country)[0]
        origin_all_airports_place = get_all_airports_place(
            self._conn, flight_filter.origin.city, origin_country, self._user_country)
        destination_country = find_in_countries(self._countries, flight_filter.destination.country)[0]
        destination_all_airports_place = get_all_airports_place(
            self._conn, flight_filter.destination.city, destination_country, self._user_country)

        all_partial_dates = utils.get_possible_partial_dates(
            flight_filter.outbound_date_not_earlier,
            flight_filter.inbound_date_not_later,
            flight_filter.approx_trip_length_days,
            flight_filter.plus_minus_days)

        currencies = {}
        carriers = {}
        places = {}
        results = []

        constraint = fc.WrappedConstraint(
            [
                fc.FlightIndicativeLengthConstraint(flight_filter.approx_trip_length_days,
                                                    flight_filter.plus_minus_days),
                fc.FlightFitsInDatesConstraint(flight_filter.outbound_date_not_earlier,
                                               flight_filter.inbound_date_not_later)
            ])

        for (outbound_pd, inbound_pd) in all_partial_dates:
            flights = self._conn.get_quotes(
                self._user_country['Code'], origin_all_airports_place['PlaceId'],
                destination_all_airports_place['PlaceId'],
                str(outbound_pd), str(inbound_pd))

            results = results + list(filter(lambda f: constraint(f), flights['Quotes']))
            places.update({x['PlaceId']: x for x in flights['Places']})
            carriers.update({x['CarrierId']: x for x in flights['Carriers']})
            currencies.update({x['Code']: x for x in flights['Currencies']})

        return results, carriers, currencies, places
