from typing import List

from utils.parameters import constants
import socket

from umodbus import conf
from umodbus.client import tcp

conf.SIGNED_VALUES = True

sockRoom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockRoom.connect(('localhost', 500))
message = tcp.write_multiple_coils(slave_id=1, starting_address=1, values=[False, False,False, False,False, False,False])
tcp.send_message(message, sockRoom)

sockWater = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockWater.connect(('localhost', 501))
message = tcp.write_multiple_coils(slave_id=1, starting_address=0, values=[False])
tcp.send_message(message, sockWater)


class Communication():
    airing: bool = False
    room_heating: List[bool] = [False, False, False, False, False, False, False]
    water_heating: bool = False

    # def turn_off_airing(self):
    #     #todo send airing on
    #
    # def turn_on_airing(self):
    #     #todo send airing off

    def water_heater_on_off(self, state: bool):
        message = tcp.write_multiple_coils(slave_id=1, starting_address=1, values=state)
        self.water_heating = bool(tcp.send_message(message, sockWater))

    def room_heating_off(self):
        message = tcp.write_multiple_coils(slave_id=1, starting_address=1,
                                           values=[False, False, False, False, False, False, False])
        tcp.send_message(message, sockRoom)
        self.room_heating = [False, False, False, False, False, False, False]

    def turn_on_room_heating(self, kw: float):
        sums: dict = self.get_possible_sums()
        powers: List[float] = []
        for key in sums:
            if len(powers) == 0:
                powers = sums[key]
            elif sums[key] == kw:
                powers = sums[key]
                break
            elif abs(kw - self.sum_of_powers(sums[key])) < abs(
                    kw - self.sum_of_powers(powers)) and kw - self.sum_of_powers(sums[key]) > 0:
                powers = sums[key]

        for pow in powers:
            self.room_heating[constants.heat_power_per_room.index(pow)] = True
            message = tcp.write_multiple_coils(slave_id=1, starting_address=1,
                                               values=self.room_heating)
            print(tcp.send_message(message, sockRoom))

    def get_possible_sums(self) -> dict:
        sums: dict = {}
        for i in range(len(constants.heat_power_per_room) - 1):
            powers: List[float] = []
            powers.append(constants.heat_power_per_room[i])
            sums[self.sum_of_powers(powers)] = powers.copy()
            for j in range(i + 1, len(constants.heat_power_per_room) - 1):
                powers.append(constants.heat_power_per_room[j])
                sums[self.sum_of_powers(powers)] = powers.copy()

        return sums

    def sum_of_powers(self, powers: List[float]) -> float:
        if len(powers) == 0:
            return 0
        sum_of_elems = 0
        for i in powers:
            sum_of_elems = sum_of_elems + i

        return (sum_of_elems)


if __name__ == '__main__':
    Communication().turn_on_room_heating(2.9)
