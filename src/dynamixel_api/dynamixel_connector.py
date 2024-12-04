"""
MIT License

Copyright (c) 2024 Tim Schneider, Erik Helmut

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import struct
import time
from abc import abstractmethod
from collections import deque
from typing import Optional, NamedTuple, Dict, Sequence

from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS, PKT_ID, PKT_ERROR

from .custom_protocol2_packet_handler import CustomProtocol2PacketHandler

Field = NamedTuple("Field", (
    ("address", int), ("data_type", str), ("name", str), ("desc", str), ("writable", bool),
    ("initial_value", Optional[int])))


# TODO: properly implement bulk reading

class DynamixelError(Exception):
    pass


class DynamixelConnectionError(DynamixelError):
    pass


class DynamixelCommunicationError(DynamixelError):
    def __init__(self, communication_result: int, packet_handler: PacketHandler, action: str):
        self.__communication_result = communication_result
        super(DynamixelCommunicationError, self).__init__("Encountered communication error during {}: {}".format(
            action, packet_handler.getTxRxResult(self.__communication_result)))

    @property
    def communication_result(self) -> int:
        return self.__communication_result


class DynamixelPacketError(DynamixelError):
    def __init__(self, error_code: int, packet_handler: PacketHandler, action: str):
        self.__error_code = error_code
        super(DynamixelPacketError, self).__init__("Encountered packet error during {}: {}".format(
            action, packet_handler.getRxPacketError(self.__error_code)))

    @property
    def error_code(self) -> int:
        return self.__error_code


class DynamixelFuture:
    def __init__(self, connector: "DynamixelConnector", packet_handler: CustomProtocol2PacketHandler,
                 port_handler: PortHandler):
        self._connector = connector
        self._packet_handler = packet_handler
        self._port_handler = port_handler

    @abstractmethod
    def _read(self, blocking: bool):
        pass

    @abstractmethod
    def result(self):
        pass


class FieldReadFuture(DynamixelFuture):
    def __init__(self, field: Field, connector: "DynamixelConnector", packet_handler: CustomProtocol2PacketHandler,
                 port_handler: PortHandler):
        super(FieldReadFuture, self).__init__(connector, packet_handler, port_handler)
        self.__field = field
        self.__data = self.__comm_result = self.__error = None
        self.__read = False

    def _read(self, blocking: bool):
        assert not self.__read
        self._port_handler.setPacketTimeoutMillis(100)
        try:
            data_raw, self.__comm_result, self.__error = self._packet_handler.readRx(
                self._port_handler, self._connector.dynamixel_id, struct.calcsize(self.__field.data_type), blocking)
            if self.__comm_result == 0 and self.__error == 0:
                self.__data = struct.unpack("<{}".format(self.__field.data_type), bytes(data_raw))[0]
            self.__read = True
        except BlockingIOError:
            pass
        return self.__read

    def result(self):
        if not self.__read:
            self._connector.process_futures(stop_on=self)
        if self.__comm_result != 0:
            raise DynamixelCommunicationError(self.__comm_result, self._packet_handler, "reading")
        elif self.__error != 0:
            raise DynamixelPacketError(self.__error, self._packet_handler, "reading")
        return self.__data


class FieldWriteFuture(DynamixelFuture):
    def __init__(self, connector: "DynamixelConnector", packet_handler: PacketHandler, port_handler: PortHandler):
        super(FieldWriteFuture, self).__init__(connector, packet_handler, port_handler)
        self.__comm_result = self.__error = None
        self.__read = False

    def _read(self, blocking: bool):
        assert not self.__read
        self._port_handler.setPacketTimeoutMillis(100)
        try:
            while True:
                rxpacket, result = self._packet_handler.rxPacket(self._port_handler, blocking=blocking)
                if result != COMM_SUCCESS or self._connector.dynamixel_id == rxpacket[PKT_ID]:
                    break

            self.__comm_result = result
            self.__error = rxpacket[PKT_ERROR] if result == COMM_SUCCESS else 0
            self.__read = True
        except BlockingIOError:
            pass
        return self.__read

    def result(self):
        if not self.__read:
            self._connector.process_futures(stop_on=self)
        if self.__comm_result != 0:
            raise DynamixelCommunicationError(self.__comm_result, self._packet_handler, "writing")
        elif self.__error != 0:
            raise DynamixelPacketError(self.__error, self._packet_handler, "writing")


class DynamixelConnector:
    def __init__(self, fields: Sequence[Field], device: str = "/dev/ttyUSB0", baud_rate: int = 57600,
                 dynamixel_id: int = 1):
        self.__baud_rate = baud_rate
        self.__dynamixel_id = dynamixel_id
        self.__device = device
        self.__port_handler: Optional[PortHandler] = None
        self.__packet_handler = CustomProtocol2PacketHandler()
        self.__field_dict = {f.name: f for f in fields}
        self.__future_queue = deque()
        self.__last_tx = 0
        self.__tx_wait_time = 0.001

    def connect(self):
        if not self.connected:
            self.__port_handler = PortHandler(self.__device)
            try:
                if not self.__port_handler.openPort():
                    self.__port_handler = None
                    raise DynamixelConnectionError("Failed to open port.")

                if not self.__port_handler.setBaudRate(self.__baud_rate):
                    self.disconnect()
                    raise DynamixelConnectionError("Failed to set baud rate.")
            except Exception as e:
                self.__port_handler = None
                raise

    def disconnect(self):
        if self.connected:
            self.__port_handler.closePort()
            self.__port_handler = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def read_field_async(self, field_name: str):
        if not self.connected:
            raise DynamixelError("Controller is not connected.")
        field = self.__field_dict[field_name]
        # Not waiting between two transmissions causes the controller to not reply
        now = time.time()
        time.sleep(max(0.0, self.__tx_wait_time - (now - self.__last_tx)))
        comm_result = self.__packet_handler.readTx(
            self.__port_handler, self.__dynamixel_id, field.address, struct.calcsize(field.data_type))
        self.__last_tx = time.time()
        self.__port_handler.is_using = False
        if comm_result != 0:
            raise DynamixelCommunicationError(comm_result, self.__packet_handler, "reading")
        future = FieldReadFuture(field, self, self.__packet_handler, self.__port_handler)
        self.__future_queue.append(future)
        self.process_futures(blocking=False)
        return future

    def write_field_async(self, field_name: str, value: int):
        if not self.connected:
            raise DynamixelError("Controller is not connected.")
        field = self.__field_dict[field_name]
        data = list(struct.pack("<{}".format(field.data_type), value))
        # Not waiting between two transmissions causes the controller to not reply
        now = time.time()
        time.sleep(max(0.0, self.__tx_wait_time - (now - self.__last_tx)))
        comm_result = self.__packet_handler.writeTxOnly(
            self.__port_handler, self.__dynamixel_id, field.address, len(data), data)
        self.__last_tx = time.time()
        self.__port_handler.is_using = False
        if comm_result != 0:
            raise DynamixelCommunicationError(comm_result, self.__packet_handler, "writing")
        future = FieldWriteFuture(self, self.__packet_handler, self.__port_handler)
        self.__future_queue.append(future)
        self.process_futures(blocking=False)
        return future

    def read_field(self, field_name: str):
        return self.read_field_async(field_name).result()

    def write_field(self, field_name: str, value: int):
        return self.write_field_async(field_name, value).result()

    def process_futures(self, stop_on: Optional[DynamixelFuture] = None, blocking: bool = True):
        while len(self.__future_queue) > 0:
            future = self.__future_queue[0]
            if future._read(blocking):
                self.__future_queue.popleft()
            else:
                break
            if future == stop_on:
                break

    @property
    def connected(self):
        return self.__port_handler is not None

    @property
    def fields(self) -> Dict[str, Field]:
        return self.__field_dict

    @property
    def dynamixel_id(self) -> int:
        return self.__dynamixel_id
