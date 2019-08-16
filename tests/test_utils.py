from find_my_flight.services.utils import left_join_flights, get_possible_partial_dates
import unittest
import datetime as dt
from find_my_flight.model.model import PartialDate as PD


class UtilsTestCase(unittest.TestCase):
    def test_left_join_flights(self):
        left = [1,2,3]
        right = [2, 3, 3, 6]
        condition = lambda x, y: x == y
        expected = [(1,[]), (2,[2]), (3, [3, 3])]
        actual = left_join_flights(left, right, condition)

        self.assertEqual(expected, actual)

    def test_get_possible_partial_dates1(self):
        earliest = dt.date(2019, 12, 21)
        latest = dt.date(2020, 1, 20)
        length = 15
        error = 3

        actual = get_possible_partial_dates(earliest, latest, length, error)
        expected = [(PD(2019,12), PD(2020,1)), (PD(2020,1), PD(2020, 1))]

        self.assertEqual(expected, actual)

    def test_get_possible_partial_dates2(self):
        earliest = dt.date(2019, 12, 21)
        latest = dt.date(2020, 1, 20)
        length = 21
        error = 0

        actual = get_possible_partial_dates(earliest, latest, length, error)
        expected = [(PD(2019,12), PD(2020,1))]

        self.assertEqual(expected, actual)