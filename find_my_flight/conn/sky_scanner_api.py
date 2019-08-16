import hashlib
import json
import pathlib
import typing
from abc import ABCMeta, abstractmethod, ABC

import requests

DEFAULT_LOCALE = 'en-US'
HOST = 'skyscanner-skyscanner-flight-search-v1.p.rapidapi.com'

ListOfDict = typing.List[typing.Dict]


class SkyScannerApiInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_countries(self, locale=DEFAULT_LOCALE):
        pass

    @abstractmethod
    def get_places(self, country, city, cur='EUR', locale=DEFAULT_LOCALE):
        """
        [{"PlaceId":"SCQ-sky","PlaceName":"Santiago de Compostela","CountryId":"ES-sky","RegionId":"","CityId":"SANC-sky","CountryName":"Spain"},{"PlaceId":"SCLA-sky","PlaceName":"Santiago","CountryId":"CL-sky","RegionId":"","CityId":"SCLA-sky","CountryName":"Chile"},{"PlaceId":"SCL-sky","PlaceName":"Santiago Arturo Merino Benitez","CountryId":"CL-sky","RegionId":"","CityId":"SCLA-sky","CountryName":"Chile"},{"PlaceId":"ULC-sky","PlaceName":"Santiago Los Cerrillos","CountryId":"CL-sky","RegionId":"","CityId":"SCLA-sky","CountryName":"Chile"},{"PlaceId":"CLO-sky","PlaceName":"Cali","CountryId":"CO-sky","RegionId":"","CityId":"CLOA-sky","CountryName":"Colombia"},{"PlaceId":"SCU-sky","PlaceName":"Santiago","CountryId":"CU-sky","RegionId":"","CityId":"SCUA-sky","CountryName":"Cuba"},{"PlaceId":"STI-sky","PlaceName":"Santiago","CountryId":"DO-sky","RegionId":"","CityId":"STIA-sky","CountryName":"Dominican Republic"},{"PlaceId":"QRO-sky","PlaceName":"Queretaro","CountryId":"MX-sky","RegionId":"","CityId":"QUEA-sky","CountryName":"Mexico"},{"PlaceId":"SDE-sky","PlaceName":"Santiago Del Estero","CountryId":"AR-sky","RegionId":"","CityId":"SDEA-sky","CountryName":"Argentina"},{"PlaceId":"PNO-sky","PlaceName":"Pinotepa Nacional","CountryId":"MX-sky","RegionId":"","CityId":"PNOA-sky","CountryName":"Mexico"}]
        :param country:
        :param city:
        :param cur:
        :param locale:
        :return:
        """
        pass

    @abstractmethod
    def get_quotes(self, country, origin_place, destination_place, outbound_date, inbound_date, cur='EUR',
                   locale=DEFAULT_LOCALE):
        pass


class SkyScannerAPI(SkyScannerApiInterface):
    def __init__(self, key, project=None):
        self._project = project
        self._key = key

    def get_countries(self, locale=DEFAULT_LOCALE) -> ListOfDict:
        host = HOST
        response = requests.get(
            'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/reference/v1.0/countries/en-US',
            headers=
            {
                "X-RapidAPI-Host": host,
                "X-RapidAPI-Key": self._key
            })
        response.raise_for_status()
        content = json.loads(response.text, encoding=response.encoding)
        countries = content['Countries']
        return countries

    def get_places(self, country, city, cur='EUR', locale=DEFAULT_LOCALE):
        """
        [{"PlaceId":"SCQ-sky","PlaceName":"Santiago de Compostela","CountryId":"ES-sky","RegionId":"","CityId":"SANC-sky","CountryName":"Spain"},{"PlaceId":"SCLA-sky","PlaceName":"Santiago","CountryId":"CL-sky","RegionId":"","CityId":"SCLA-sky","CountryName":"Chile"},{"PlaceId":"SCL-sky","PlaceName":"Santiago Arturo Merino Benitez","CountryId":"CL-sky","RegionId":"","CityId":"SCLA-sky","CountryName":"Chile"},{"PlaceId":"ULC-sky","PlaceName":"Santiago Los Cerrillos","CountryId":"CL-sky","RegionId":"","CityId":"SCLA-sky","CountryName":"Chile"},{"PlaceId":"CLO-sky","PlaceName":"Cali","CountryId":"CO-sky","RegionId":"","CityId":"CLOA-sky","CountryName":"Colombia"},{"PlaceId":"SCU-sky","PlaceName":"Santiago","CountryId":"CU-sky","RegionId":"","CityId":"SCUA-sky","CountryName":"Cuba"},{"PlaceId":"STI-sky","PlaceName":"Santiago","CountryId":"DO-sky","RegionId":"","CityId":"STIA-sky","CountryName":"Dominican Republic"},{"PlaceId":"QRO-sky","PlaceName":"Queretaro","CountryId":"MX-sky","RegionId":"","CityId":"QUEA-sky","CountryName":"Mexico"},{"PlaceId":"SDE-sky","PlaceName":"Santiago Del Estero","CountryId":"AR-sky","RegionId":"","CityId":"SDEA-sky","CountryName":"Argentina"},{"PlaceId":"PNO-sky","PlaceName":"Pinotepa Nacional","CountryId":"MX-sky","RegionId":"","CityId":"PNOA-sky","CountryName":"Mexico"}]
        :param country:
        :param city:
        :param cur:
        :param locale:
        :return:
        """

        response = requests.get(
            f'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/{country}/{cur}/{locale}/?query={city}',
            headers=
            {
                "X-RapidAPI-Host": HOST,
                "X-RapidAPI-Key": self._key
            })
        response.raise_for_status()
        places = json.loads(response.text, encoding=response.encoding)['Places']
        return places

    def get_quotes(
            self, country, origin_place, destination_place, outbound_date, inbound_date, cur='EUR',
            locale=DEFAULT_LOCALE):
        response = requests.get(
            f'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/{country}/{cur}/{locale}/{origin_place}/{destination_place}/{outbound_date}/{inbound_date}',
            headers=
            {
                "X-RapidAPI-Host": HOST,
                "X-RapidAPI-Key": self._key
            })
        response.raise_for_status()
        quotes = json.loads(response.text, encoding=response.encoding)
        return quotes

    def get_routes_inbound(
            self, country, origin_place, destination_place, outbound_date: str, inbound_date: str, cur: str = 'EUR',
            locale=DEFAULT_LOCALE):
        response = requests.get(
            f'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/'
            f'{country}/{cur}/{locale}/{origin_place}/{destination_place}/{outbound_date}/{inbound_date}',
            headers=
            {
                "X-RapidAPI-Host": HOST,
                "X-RapidAPI-Key": self._key
            })
        response.raise_for_status()
        routes = json.loads(response.text, encoding=response.encoding)
        return routes


class cached(object):
    def __init__(self, cache_location):
        self.cache_location = pathlib.Path(cache_location)

    def __call__(self, f):
        def cached_decorator(*args, **kwargs):
            parameters = {'args': args, 'kwargs': kwargs}
            hashed_json = hashlib.md5(f'{f.__name__}_{json.dumps(parameters)}')
            cache = self.cache_location / hashed_json
            if cache.exists():
                with cache.open() as c:
                    return c.read()
            else:
                res = f(*args, **kwargs)
                with cache.open('w') as c:
                    c.write(res)
                return res

        return cached_decorator


class CachedExecutor:
    def __init__(self, cache_location):
        self.cache_location = pathlib.Path(cache_location)

    def run(self, f, *args, **kwargs):
        parameters = {'args': args, 'kwargs': kwargs}
        hashed_json = hashlib.md5(f'{f.__name__}_{json.dumps(parameters, default=str)}'.encode('utf-8')).hexdigest()
        cache = self.cache_location / f'{str(hashed_json)}.json'
        if cache.exists():
            with cache.open() as c:
                return json.load(c)
        else:
            res = f(*args, **kwargs)
            with cache.open('w') as c:
                c.write(json.dumps(res))
            return res


# todo: class decorator?
class CachedSkyScannerAPI(SkyScannerApiInterface, ABC):
    def __init__(self, conn: SkyScannerApiInterface, cache_location):
        self.conn = conn
        self.cache_executor = CachedExecutor(cache_location)

    def get_countries(self, locale=DEFAULT_LOCALE):
        return self.cache_executor.run(self.conn.get_countries, locale)

    def get_places(self, country, city, cur='EUR', locale=DEFAULT_LOCALE):
        return self.cache_executor.run(self.conn.get_places, country, city, cur, locale)

    def get_quotes(self, country, origin_place, destination_place, outbound_date, inbound_date, cur='EUR',
                   locale=DEFAULT_LOCALE):
        return self.cache_executor.run(
            self.conn.get_quotes,
            country, origin_place, destination_place, outbound_date, inbound_date, cur, locale)
