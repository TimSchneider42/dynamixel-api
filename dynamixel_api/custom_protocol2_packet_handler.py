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
from dynamixel_sdk import Protocol2PacketHandler, PortHandler, COMM_TX_FAIL, COMM_SUCCESS, COMM_RX_TIMEOUT, \
    COMM_RX_CORRUPT, DXL_MAKEWORD, PKT_RESERVED, PKT_ID, PKT_INSTRUCTION, PKT_LENGTH_L, PKT_LENGTH_H, RXPACKET_MAX_LEN, \
    PKT_ERROR, PKT_PARAMETER0


class CustomProtocol2PacketHandler(Protocol2PacketHandler):
    """
    A packet handler that provides a blocking parameter for the rxPacket function.
    """

    def __init__(self):
        self.__rx_buffer = []
        super(CustomProtocol2PacketHandler, self).__init__()

    def rxPacket(self, port: PortHandler, blocking: bool = True):
        result = None
        # minimum length (HEADER0 HEADER1 HEADER2 RESERVED ID LENGTH_L LENGTH_H INST ERROR CRC16_L CRC16_H)
        wait_length = 11

        while result is None:
            read_len = wait_length - len(self.__rx_buffer)
            new_data = port.readPort(read_len)
            self.__rx_buffer.extend(new_data)
            if len(new_data) <= read_len and not blocking:
                raise BlockingIOError("Packet not received completely yet.")
            if len(self.__rx_buffer) >= wait_length:
                # find packet header
                idx = 0
                while idx < len(self.__rx_buffer) - 3 and \
                        (self.__rx_buffer[idx:idx + 3] != [0xFF, 0xFF, 0xFD] or self.__rx_buffer[idx + 3] == 0xFD):
                    idx += 1

                if idx == 0:
                    packet_len_header = DXL_MAKEWORD(self.__rx_buffer[PKT_LENGTH_L], self.__rx_buffer[PKT_LENGTH_H])
                    if self.__rx_buffer[PKT_RESERVED] != 0x00 or self.__rx_buffer[PKT_ID] > 0xFC or \
                            packet_len_header > RXPACKET_MAX_LEN or self.__rx_buffer[PKT_INSTRUCTION] != 0x55:
                        # remove the first byte in the packet
                        self.__rx_buffer[:1] = []
                    elif wait_length != packet_len_header + PKT_LENGTH_H + 1:
                        wait_length = packet_len_header + PKT_LENGTH_H + 1
                    elif len(self.__rx_buffer) < wait_length:
                        if port.isPacketTimeout():
                            result = COMM_RX_TIMEOUT if len(self.__rx_buffer) == 0 else COMM_RX_CORRUPT
                    else:
                        crc = DXL_MAKEWORD(self.__rx_buffer[wait_length - 2], self.__rx_buffer[wait_length - 1])
                        computed_crc = self.updateCRC(0, self.__rx_buffer, wait_length - 2)
                        result = COMM_SUCCESS if computed_crc == crc else COMM_RX_CORRUPT
                else:
                    # remove unnecessary bytes
                    self.__rx_buffer[:idx] = []
            else:
                if port.isPacketTimeout():
                    result = COMM_RX_TIMEOUT if len(self.__rx_buffer) == 0 else COMM_RX_CORRUPT

        port.is_using = False

        rx_packet = self.__rx_buffer
        self.__rx_buffer = []
        if result == COMM_SUCCESS:
            rx_packet = self.removeStuffing(rx_packet)

        return rx_packet, result

    def readRx(self, port: PortHandler, dxl_id: int, length: int, blocking: bool = True):
        error = 0
        data = []

        while True:
            rxpacket, result = self.rxPacket(port, blocking=blocking)
            if result != COMM_SUCCESS or rxpacket[PKT_ID] == dxl_id:
                break

        if result == COMM_SUCCESS and rxpacket[PKT_ID] == dxl_id:
            error = rxpacket[PKT_ERROR]
            data.extend(rxpacket[PKT_PARAMETER0 + 1: PKT_PARAMETER0 + 1 + length])

        return data, result, error
