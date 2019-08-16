import unittest
import find_my_flight.model.flight_constraint as fc

class FlightConstraintTestCase(unittest.TestCase):
    def test_inner_flight_constraint(self):
        f1 = {'OutboundLeg': {'DepartureDate': '2020-01-01T00:00:00'}, 'InboundLeg': {'DepartureDate': '2020-01-19T00:00:00'}}
        target = fc.InnerFlightConstraint(f1, 1)
        f2 = {'OutboundLeg': {'DepartureDate': '2020-01-03T00:00:00'}, 'InboundLeg': {'DepartureDate': '2020-01-15T00:00:00'}}
        self.assertTrue(target(f2))

    def test_inner_flight_constraint_too_short_slack(self):
        f1 = {'OutboundLeg': {'DepartureDate': '2020-01-01T00:00:00'}, 'InboundLeg': {'DepartureDate': '2020-01-19T00:00:00'}}
        target = fc.InnerFlightConstraint(f1, 2)
        f2 = {'OutboundLeg': {'DepartureDate': '2020-01-03T00:00:00'}, 'InboundLeg': {'DepartureDate': '2020-01-15T00:00:00'}}
        self.assertFalse(target(f2))
