
import socket

from umodbus import conf
from umodbus.client import tcp

conf.SIGNED_VALUES = True

sockWater = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockWater.connect(('localhost', 501))
message = tcp.write_multiple_coils(slave_id=1, starting_address=0, values=[False])
tcp.send_message(message, sockWater)
sockWater.close()

sockRoom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockRoom.connect(('localhost', 500))
message = tcp.write_multiple_coils(slave_id=1, starting_address=1, values=[False, False,False, False,False, False,False])
tcp.send_message(message, sockRoom)
sockRoom.close()