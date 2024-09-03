# OysterCard class and other related classes

import unittest
from Oyster_Card import Station, Journey, OysterCard


class TestOysterCardSystem(unittest.TestCase):
    
    def setUp(self):
        # Set up some test stations
        self.holborn = Station("Holborn", [1])
        self.earls_court = Station("Earl's Court", [1, 2])
        self.hammersmith = Station("Hammersmith", [2])
        self.wimbledon = Station("Wimbledon", [3])

        # Set up an Oyster card with a starting balance
        self.card = OysterCard(balance=30)
    
    def test_station_initialization(self):
        # Test station initialization
        station = Station("Test Station", [1, 2])
        self.assertEqual(station.name, "Test Station")
        self.assertEqual(station.zones, [1, 2])

    def test_journey_initialization(self):
        # Test journey initialization
        journey = Journey(start_station=self.holborn, end_station=self.earls_court)
        self.assertEqual(journey.start_station, self.holborn)
        self.assertEqual(journey.end_station, self.earls_court)

    def test_load_balance(self):
        # Test loading balance onto the card
        self.card.load_balance(10)
        self.assertEqual(self.card.balance, 40)

    def test_insufficient_balance_swipe_in(self):
        # Test swiping in with insufficient balance
        low_balance_card = OysterCard(balance=2)
        low_balance_card.swipe_in(self.holborn)
        self.assertIsNone(low_balance_card.current_journey)  # No journey should start

    def test_swipe_in_and_out_zone_1(self):
        # Test a journey from Holborn to Earl's Court within Zone 1
        self.card.swipe_in(self.holborn)
        self.card.swipe_out(self.earls_court)
        self.assertEqual(self.card.balance, 30 - 2.50)

    def test_swipe_in_and_out_zone_2(self):
        # Test a journey from Earl's Court to Hammersmith (Zone 2)
        self.card.swipe_in(self.earls_court)
        self.card.swipe_out(self.hammersmith)
        self.assertEqual(self.card.balance, 30 - 2.25)

    def test_swipe_in_and_out_zone_3(self):
        # Test a journey from Earl's Court to Wimbledon (crossing multiple zones)
        self.card.swipe_in(self.earls_court)
        self.card.swipe_out(self.wimbledon)
        self.assertEqual(self.card.balance, 30 - 3.20)

    def test_swipe_in_and_out_same_station(self):
        # Test a journey where the user swipes in and out at the same station
        self.card.swipe_in(self.earls_court)
        self.card.swipe_out(self.earls_court)
        self.assertEqual(self.card.balance, 30 - 2.50)

    def test_take_bus(self):
        # Test taking a bus journey
        self.card.take_bus()
        self.assertEqual(self.card.balance, 30 - 1.80)

    def test_swipe_out_without_swipe_in(self):
        # Test swiping out without swiping in
        self.card.swipe_out(self.holborn)
        self.assertEqual(self.card.balance, 30 - 3.20)  # Maximum fare charged

    def test_invalid_station_swipe_out(self):
        # Test swiping out with an invalid station
        self.card.swipe_in(self.holborn)
        self.card.swipe_out(None)
        self.assertEqual(self.card.balance, 30 - 3.20)  # Maximum fare charged


if __name__ == '__main__':
    unittest.main()
