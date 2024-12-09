"""
MIT License

Copyright (c) 2021 Tim Schneider

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

import warnings

from ..dynamixel_connector import DynamixelConnector, Field

RHP12RN_EEPROM_FIELDS = [
    Field(0, "H", "model_number", "Model Number", False, 35073),
    Field(2, "i", "model_information", "Model Information", False, None),
    Field(6, "B", "firmware_version", "Firmware Version", False, None),
    Field(7, "B", "id", "DYNAMIXEL ID", True, 1),
    Field(8, "B", "baud_rate", "Communication Speed", True, 1),
    Field(9, "B", "return_delay_time", "Response Delay Time", True, 250),
    Field(11, "B", "operating_mode", "Operating Mode", True, 5),
    Field(17, "i", "moving_threshold", "Velocity Threshold for Movement Detection", True, 10),
    Field(21, "B", "temperature_limit", "Maximum Internal Temperature Limit", True, 80),
    Field(22, "H", "max_voltage_limit", "Maximum Input Voltage Limit", True, 400),
    Field(24, "H", "min_voltage_limit", "Minimum Input Voltage Limit", True, 150),
    Field(26, "i", "acceleration_limit", "Maximum Accleration Limit", True, 255),
    Field(30, "H", "current_limit", "Maximum Current Limit", True, 820),
    Field(32, "i", "velocity_limit", "Maximum Velocity Limit", True, 100),
    Field(36, "i", "max_position_limit", "Maximum Position Limit", True, 1150),
    Field(40, "i", "min_position_limit", "Minimum Position Limit", True, 0),
    Field(44, "B", "external_port_mode_1", "External Port Mode 1", True, 0),
    Field(45, "B", "external_port_mode_2", "External Port Mode 2", True, 0),
    Field(46, "B", "external_port_mode_3", "External Port Mode 3", True, 0),
    Field(47, "B", "external_port_mode_4", "External Port Mode 4", True, 0),
    Field(48, "B", "shutdown", "Shutdown Error Information", True, 48)
]

RHP12RN_EEPROM_FIELDS += [
    Field(49 + i * 2, "H", "indirect_address_{}".format(i + 1), "Indirect Address {}".format(i + 1), True, 634 + i)
    for i in range(256)
]

RHP12RN_RAM_FIELDS = [
    Field(562, "B", "torque_enable", "Motor Torque On/Off", True, 0),
    Field(563, "B", "led_red", "Red LED Intensity Value", True, 0),
    Field(564, "B", "led_green", "Green LED Intensity Value", True, 0),
    Field(565, "B", "led_blue", "Blue LED Intensity Value", True, 0),
    Field(590, "H", "position_d_gain", "D Gain of Position", True, None),
    Field(592, "H", "position_i_gain", "I Gain of Position", True, None),
    Field(594, "H", "position_p_gain", "P Gain of Position", True, None),
    Field(596, "i", "goal_position", "Target Position Value", True, None),
    Field(600, "i", "goal_velocity", "Target Velocity Value", True, 0),
    Field(604, "H", "goal_current", "Target Current Value", True, 0),
    Field(606, "i", "goal_acceleration", "Target Acceleration Value", True, 0),
    Field(610, "B", "moving", "Movement Status", False, None),
    Field(611, "i", "present_position", "Present Position Value", False, None),
    Field(615, "i", "present_velocity", "Present Velocity Value", False, None),
    Field(621, "H", "present_current", "Present Current Value", False, None),
    Field(623, "H", "present_input_voltage", "Present Input Voltage", False, None),
    Field(625, "B", "present_temperature", "Present Internal Temperature", False, None),
    Field(626, "H", "external_port_data_1", "External Port Data 1", True, 0),
    Field(628, "H", "external_port_data_2", "External Port Data 2", True, 0),
    Field(630, "H", "external_port_data_3", "External Port Data 3", True, 0),
    Field(632, "H", "external_port_data_4", "External Port Data 4", True, 0)
]

RHP12RN_RAM_FIELDS += [
    Field(634 + i, "B", "indirect_data_{}".format(i + 1), "Indirect Data {}".format(i + 1), True, 0) for i in range(256)
]

RHP12RN_RAM_FIELDS += [
    Field(890, "B", "registered_instruction", "Check Reception of Instruction", False, 0),
    Field(891, "B", "status_return_level", "Select Types of Status Return", True, 2),
    Field(892, "B", "hardware_error_status", "Hardware Error Status", False, 0)
]

RHP12RN_FIELDS = RHP12RN_EEPROM_FIELDS + RHP12RN_RAM_FIELDS


class RHP12RNConnector(DynamixelConnector):
    def __init__(self, device: str = "/dev/ttyUSB0", baud_rate: int = 57600, dynamixel_id: int = 1):
        super(RHP12RNConnector, self).__init__(
            RHP12RN_FIELDS, device=device, baud_rate=baud_rate, dynamixel_id=dynamixel_id)

    def connect(self):
        super(RHP12RNConnector, self).connect()
        model_number = self.read_field("model_number")
        if model_number != self.fields["model_number"].initial_value:
            warnings.warn("The connected device does not appear to be a RH-P12-RN gripper.")
