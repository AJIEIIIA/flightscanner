import unittest
from find_my_flight.main import PartialDate, get_inner_flight_partial_dates


class PartialDateTestCase(unittest.TestCase):
    def test_get_inner_partial_dates(self):
        pd0 = PartialDate(2019, 12)
        pd1 = PartialDate(2020, 1)

        target = get_inner_flight_partial_dates(pd0, pd1, 3)
        self.assertEqual(target, [
            (PartialDate(2019, 12), PartialDate(2019, 12)),
            (PartialDate(2019, 12), PartialDate(2020, 1)),
            (PartialDate(2020, 1), PartialDate(2020, 1))
        ])