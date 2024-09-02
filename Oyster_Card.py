class Station:
    def __init__(self, name, zones):
        """
        Initialize a station with a name and zones.
        :param name: Name of the station.
        :param zones: List of zones the station belongs to.
        """
        self.name = name
        self.zones = zones


class Journey:
    def __init__(self, start_station=None, end_station=None):
        """
        Initialize a journey with a start and an optional end station.
        :param start_station: The station where the journey starts.
        :param end_station: The station where the journey ends.
        """
        self.start_station = start_station
        self.end_station = end_station


class OysterCard:
    MAX_FARE = 3.20  # Maximum possible fare
    BUS_FARE = 1.80  # Flat rate for bus journeys

    def __init__(self, balance=0.0):
        self.balance = balance
        self.current_journey = None
        self.max_fare_charged = False

    def load_balance(self, amount):
        self.balance += amount
        print(f"Loaded £{amount}. Current balance: £{self.balance}")

    def swipe_in(self, station):
        if self.balance < self.MAX_FARE:
            print(f"Insufficient balance for maximum fare (£{self.MAX_FARE}). Access denied.")
            return
        if self.current_journey is not None:
            print(f"Warning: Previous journey incomplete. Charging maximum fare of £{self.MAX_FARE}.")
            self.balance -= self.MAX_FARE
            self.current_journey = None
            print(f"Current balance after penalty: £{self.balance}")

        self.current_journey = Journey(start_station=station)
        self.balance -= self.MAX_FARE
        self.max_fare_charged = True
        print(f"Swiped in at {station.name}. Maximum fare of £{self.MAX_FARE} charged. Current balance: £{self.balance}")

    def swipe_out(self, station):
        if self.current_journey is None:
            print(f"Error: Swipe out detected without a swipe in. Charging maximum fare of £{self.MAX_FARE}.")
            self.balance -= self.MAX_FARE
            print(f"Current balance after penalty: £{self.balance}")
            return

        if station is None or not isinstance(station, Station):
            print("Error: Invalid station. Charging maximum fare as penalty.")
            self.balance -= self.MAX_FARE
            self.current_journey = None
            print(f"Current balance after penalty: £{self.balance}")
            return

        self.current_journey.end_station = station
        actual_fare = self.calculate_fare(self.current_journey.start_station, station)
        refund = self.MAX_FARE - actual_fare
        self.balance += refund
        self.max_fare_charged = False
        print(f"Swiped out at {station.name}. Fare adjusted to £{actual_fare}. Refund: £{refund}. Current balance: £{self.balance}")
        self.current_journey = None

    def calculate_fare(self, start_station, end_station):
        # Copy the start and end zones to modify them if Earl's Court is involved
        start_zones = set(start_station.zones)
        end_zones = set(end_station.zones)
        
        # Adjust for Earl's Court to minimize fare
        if start_station.name == "Earl's Court":
            # Treat Earl's Court as Zone 2 if the end station is in Zone 2
            if any(zone >= 2 for zone in end_zones):
                start_zones = {2}
            # Treat Earl's Court as Zone 1 if the end station is in Zone 1
            elif 1 in end_zones:
                start_zones = {1}
        
        if end_station.name == "Earl's Court":
            # Treat Earl's Court as Zone 2 if the start station is in Zone 2
            if any(zone >= 2 for zone in start_zones):
                end_zones = {2}
            # Treat Earl's Court as Zone 1 if the start station is in Zone 1
            elif 1 in start_zones:
                end_zones = {1}

        combined_zones = start_zones.union(end_zones)
        traveled_zones = (max(combined_zones) - min(combined_zones) + 1)

        # If the user swipes out at the same station they swiped in, charge the minimum fare
        if start_station.name == end_station.name:
            return 2.50 if 1 in start_zones else 2.00

        # If the journey is entirely within Zone 1
        if combined_zones == {1}:
            return 2.50

        # If the journey is within a single zone outside Zone 1
        if traveled_zones == 1 and 1 not in combined_zones:
            return 2.00
        
        # If the journey spans two zones and excludes Zone 1
        if traveled_zones == 2 and 1 not in combined_zones:
            return 2.25

        # If the journey spans two zones and includes Zone 1
        if traveled_zones == 2 and 1 in combined_zones:
            return 3.00

        # If the journey spans three different zones
        if traveled_zones == 3:
            return 3.20

        # Default case (shouldn't be hit, but for safety)
        return 3.20

    def take_bus(self):
        if self.balance < self.BUS_FARE:
            print(f"Insufficient balance for bus fare (£{self.BUS_FARE}). Access denied.")
            return
        self.balance -= self.BUS_FARE
        print(f"Bus fare of £{self.BUS_FARE} charged. Current balance: £{self.balance}")


if __name__ == "__main__":
    # Define stations
    holborn = Station("Holborn", [1])
    earls_court = Station("Earl's Court", [1, 2])
    hammersmith = Station("Hammersmith", [2])
    wimbledon = Station('Wimbledon', [3])

    # Initialize Oyster card with £30
    card = OysterCard(balance=30)
    print(f"Initial balance: £{card.balance}")

    # 1. Tube: Holborn to Earl’s Court
    card.swipe_in(holborn)
    card.swipe_out(earls_court)  # Should charge £2.50
    print(f"Balance after Holborn to wimbledon: £{card.balance}")

    # 2. Bus: 328 bus from Earl’s Court to Chelsea (Fixed fare)
    card.take_bus()
    print(f"Balance after bus journey: £{card.balance}")

    # 3. Tube: Earl’s Court to Hammersmith
    card.swipe_in(earls_court)
    card.swipe_out(wimbledon)  # Should charge £2.25
    print(f"Final balance: £{card.balance}")