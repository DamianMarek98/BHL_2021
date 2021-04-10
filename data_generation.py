from datetime import datetime
from utils.parameters.constants import *
from utils.parameters.other_devices import get_other_devices_consumption
from utils.parameters.temperature import get_power_temp_parameter, get_expected_temperature, get_new_temperature
from utils.parameters.photovoltaics import get_photovoltaics_production
from utils.parameters.costs import get_energy_cost


class Simulator:

    datetime: datetime = datetime.now()

    # Balance
    cash_balance: float = 0

    # Water heated in liters today
    water_heated: float = 0
    is_heating_water: bool = False
    water_heat_power: float = 0

    # Heating / holding temperature
    is_heating: bool = False
    is_holding: bool = False
    heat_power: float = 0

    # Weather
    temperature_inside: float = 21
    temperature_outside: float = 20
    cloud_percentage: float = 80

    # Accumulator
    accu_is_in_use: bool = False
    accumulator_state: float = 0

    # Mode
    power_supply_mode: int = 0

    def _next_hour_used_power(self) -> float:
        power = 0
        heating_power = 0

        # Water heating.
        if self.is_heating_water:
            self.water_heat_power = max_power_water_heater
            power += self.water_heat_power
        else:
            self.water_heat_power = 0

        # Recuperation.
        recuperaiton_cost = get_other_devices_consumption(self.datetime)
        power += recuperaiton_cost
        free_heating_power = recuperaiton_cost * 0.7

        # Heating.
        if self.is_heating:
            heat_needed = get_power_temp_parameter(
                self.temperature_outside, "heat")
            if heat_needed == None:
                self.heat_power = free_heating_power
            else:
                addidtional_heat_power = min(max_power_combined_heaters -
                                             self.water_heat_power, heat_needed)
                self.heat_power = addidtional_heat_power + free_heating_power
                power += self.heat_power
        # Holding
        elif self.is_holding:
            hold_needed = get_power_temp_parameter(
                self.temperature_outside, "hold") - free_heating_power
            additional_heating_power = min(
                max_power_combined_heaters - self.is_heating_water, hold_needed)
            self.heat_power = additional_heating_power + free_heating_power
            power += additional_heating_power
        else:
            self.heat_power = 0

        return power

    def _next_hour_produced_power(self):
        power = 0

        # Photovoltaics
        power += get_photovoltaics_production(self.datetime,
                                              self.cloud_percentage)

        # Accumulator
        if self.accu_is_in_use:
            power += max_accumulator_consumption

        return power

    def update_next_temperature_by_simulation(self):
        self.temperature_inside = get_new_temperature(
            self.temperature_inside, self.temperature_outside, self.heat_power, self.datetime)

    def _update_parameters(self, temperature, cloud_percentage, datetime):

        self.temperature_outside = temperature
        self.cloud_percentage = cloud_percentage
        self.datetime = datetime

        # Update temperature operations.
        expected_temperature = get_expected_temperature(self.datetime)
        if self.temperature_inside <= expected_temperature:
            if self.temperature_outside <= expected_temperature:
                self.is_heating = True
                self.is_holding = False
            else:
                # Temperature will go up to the expected one without our involvement
                self.is_heating = False
                self.is_holding = False
        else:
            self.is_heating = False
            self.is_holding = False

    def simulate_next_hour(self, temperature, cloud_percentage, datetime):

        if datetime.hour == 0:
            self._reset_day()

        self._update_parameters(temperature, cloud_percentage, datetime)

        power_used = self._next_hour_used_power()
        power_produced = self._next_hour_produced_power()

        power_difference = power_produced - power_used

        power_unit_cost = get_energy_cost(self.datetime)
        power_unit_income = get_energy_cost(self.datetime, income=True)

        power_from_net = 0
        power_to_net = 0

        if power_unit_cost < 1:
            if power_difference > 0:
                if self.accumulator_state < max_accumulator_capacity:
                    accumulator_charge_available = min(
                        max_accumulator_capacity - self.accumulator_state, max_accumulator_charge)
                    self.accumulator_state += accumulator_charge_available
                    if accumulator_charge_available > power_difference:
                        power_from_net += accumulator_charge_available - power_difference
                    else:
                        power_to_net += power_difference - accumulator_charge_available
                else:
                    power_to_net += power_difference
            else:
                if self.accumulator_state < max_accumulator_capacity:
                    accumulator_charge_available = min(
                        max_accumulator_capacity - self.accumulator_state, max_accumulator_charge)
                    self.accumulator_state += accumulator_charge_available
                    power_from_net += accumulator_charge_available - power_difference
                else:
                    power_from_net -= power_difference
        else:
            if power_difference > 0:
                power_to_net += power_difference
            else:
                accumulator_power_available = min(
                    max_accumulator_capacity - self.accumulator_state, max_accumulator_consumption, -power_difference, 0)
                self.accumulator_state -= accumulator_power_available
                if accumulator_power_available < -power_difference:
                    power_from_net += -power_difference - accumulator_power_available

        balance = power_to_net * power_unit_income - power_from_net * power_unit_cost
        self.cash_balance += balance

        self.update_next_temperature_by_simulation()

        print(f"Power from net: {power_from_net}")
        print(f"Power to net: {power_to_net}")
        print(f"Accumulator state: {self.accumulator_state}")
        print(f"Hour balance: {balance}")
        print(f"Overall balance: {self.cash_balance}")
        print(f"Temperature inside: {self.temperature_inside}")
        print(f"Temperature outside: {self.temperature_outside}")

        return self.heat_power, self.water_heat_power, self.temperature_inside, self.power_supply_mode

    def _reset_day(self):
        self.water_heated = 0


# simulator = Simulator()
# time = datetime.now().replace(day=13, month=5)
# hour = time.hour
# simulator.simulate_next_hour(15, 82, datetime.now())
# simulator.simulate_next_hour(16, 84, datetime.now().replace(hour=hour+1))
# simulator.simulate_next_hour(18, 85, datetime.now().replace(hour=hour+2))
# simulator.simulate_next_hour(19, 86, datetime.now().replace(hour=hour+3))
# simulator.simulate_next_hour(17.7, 76, datetime.now().replace(hour=hour+4))
# simulator.simulate_next_hour(16.3, 65, datetime.now().replace(hour=hour+5))
# simulator.simulate_next_hour(10, 54, datetime.now().replace(hour=hour+6))
# simulator.simulate_next_hour(
#     10, 90, datetime.now().replace(hour=(hour+7) % 24))
# simulator.simulate_next_hour(
#     10, 90, datetime.now().replace(hour=(hour+8) % 24))
# simulator.simulate_next_hour(
#     20, 90, datetime.now().replace(hour=(hour+9) % 24))
# simulator.simulate_next_hour(
#     2, 90, datetime.now().replace(hour=(hour+10) % 24))
# simulator.simulate_next_hour(
#     2, 90, datetime.now().replace(hour=(hour+11) % 24))
# simulator.simulate_next_hour(
#     2, 90, datetime.now().replace(hour=(hour+12) % 24))
# simulator.simulate_next_hour(
#     2, 54, datetime.now().replace(hour=(hour+13) % 24))
# simulator.simulate_next_hour(
#     2, 54, datetime.now().replace(hour=(hour+14) % 24))
# simulator.simulate_next_hour(
#     2, 54, datetime.now().replace(hour=(hour+15) % 24))
# simulator.simulate_next_hour(
#     2, 54, datetime.now().replace(hour=(hour+16) % 24))
# simulator.simulate_next_hour(
#     16, 54, datetime.now().replace(hour=(hour+17) % 24))
# simulator.simulate_next_hour(
#     17, 54, datetime.now().replace(hour=(hour+18) % 24))
# simulator.simulate_next_hour(
#     15, 54, datetime.now().replace(hour=(hour+19) % 24))
# simulator.simulate_next_hour(
#     25, 54, datetime.now().replace(hour=(hour+20) % 24))
# simulator.simulate_next_hour(
#     25, 54, datetime.now().replace(hour=(hour+21) % 24))
# simulator.simulate_next_hour(
#     25, 54, datetime.now().replace(hour=(hour+22) % 24))
# simulator.simulate_next_hour(
#     25, 54, datetime.now().replace(hour=(hour+23) % 24))
