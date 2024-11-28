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

RHP12RNA_EEPROM_FIELDS = [
    Field(0, "H", "model_number", "Model Number", False, 35074),
    Field(2, "i", "model_information", "Model Information", False, None),
    Field(6, "B", "firmware_version", "Firmware Version", False, None),
    Field(7, "B", "id", "DYNAMIXEL ID", True, 1),
    Field(8, "B", "baud_rate", "Communication Speed", True, 1),
    Field(9, "B", "return_delay_time", "Response Delay Time", True, 250),
    Field(11, "B", "operating_mode", "Operating Mode", True, 5),
    Field(12, "B", "secondary_id", "Secondary ID", True, 255),
    Field(13, "B", "protocol_type", "Protocol Type", True, 2),
    Field(20, "B", "homing_offset", "Homing Offset", True, 0),
    Field(24, "i", "moving_threshold", "Velocity Threshold for Movement Detection", True, 80),
    Field(31, "B", "temperature_limit", "Maximum Internal Temperature Limit", True, 80),
    Field(32, "H", "max_voltage_limit", "Maximum Input Voltage Limit", True, 300),
    Field(34, "H", "min_voltage_limit", "Minimum Input Voltage Limit", True, 150),
    Field(36, "H", "pwm_limit", "PWM Limit", True, 2009),
    Field(38, "H", "current_limit", "Current Limit", True, 661),
    Field(40, "i", "acceleration_limit", "Maximum Accleration Limit", True, 3447),
    Field(44, "i", "velocity_limit", "Maximum Velocity Limit", True, 2970),
    Field(48, "i", "max_position_limit", "Maximum Position Limit", True, 1150),
    Field(52, "i", "min_position_limit", "Minimum Position Limit", True, 0),
    Field(56, "B", "external_port_mode_1", "External Port Mode 1", True, 3),
    Field(57, "B", "external_port_mode_2", "External Port Mode 2", True, 3),
    Field(58, "B", "external_port_mode_3", "External Port Mode 3", True, 3),
    Field(59, "B", "external_port_mode_4", "External Port Mode 4", True, 3),
    Field(63, "B", "shutdown", "Shutdown Error Information", True, 58)
]

RHP12RNA_EEPROM_FIELDS += [
    Field(168 + i * 2, "H", "indirect_address_{}".format(i + 1), "Indirect Address {}".format(i + 1), True, 634 + i)
    for i in range(128)
]

RHP12RNA_RAM_FIELDS = [
    Field(512, "B", "torque_enable", "Motor Torque On/Off", True, 0),
    Field(513, "B", "led_red", "Red LED Intensity Value", True, 0),
    Field(514, "B", "led_green", "Green LED Intensity Value", True, 0),
    Field(515, "B", "led_blue", "Blue LED Intensity Value", True, 0),
    Field(516, "B", "status_return_level", "Status Return Level", True, 2),
    Field(517, "B", "registered_instruction", "Registered Instruction", False, 0),
    Field(518, "B", "hardware_error_status", "Hardware Error Status", False, 0),
    Field(524, "H", "velocity_i_gain", "I Gain of Velocity", True, None),
    Field(526, "H", "velocity_p_gain", "P Gain of Velocity", True, None),
    Field(528, "H", "position_d_gain", "D Gain of Position", True, None),
    Field(530, "H", "position_i_gain", "I Gain of Position", True, None),
    Field(532, "H", "position_p_gain", "P Gain of Position", True, None),
    Field(536, "H", "feedforward_first_gain", "Feedforward First Gain", True, None),
    Field(538, "H", "feedforward_second_gain", "Feedforward Second Gain", True, None),
    Field(546, "B", "bus_watchdog", "Bus Watchdog", True, None),
    Field(548, "H", "goal_pwm", "Goal PWM", True, None),
    Field(550, "H", "goal_current", "Target Current Value", True, 0),
    Field(552, "i", "goal_velocity", "Target Velocity Value", True, 0),
    Field(556, "i", "profile_acceleration", "Profile Acceleration", True, 0),
    Field(560, "i", "profile_velocity", "Profile Velocity", True, 0),
    Field(564, "i", "goal_position", "Target Position Value", True, None),
    Field(568, "H", "realtime_tick", "Realtime Tick", False, None),
    Field(570, "B", "moving", "Moving", False, None),
    Field(571, "B", "moving_status", "Movement Status", False, None),
    Field(572, "H", "present_pwm", "Present PWM Value", False, None),
    Field(574, "H", "present_current", "Present Current Value", False, None),
    Field(576, "i", "present_velocity", "Present Velocity Value", False, None),
    Field(580, "i", "present_position", "Present Position Value", False, None),
    Field(584, "i", "velocity_trajectory", "Velocity Trajectory", False, None),
    Field(588, "i", "position_trajectory", "Position Trajectory", False, None),
    Field(592, "H", "present_input_voltage", "Present Input Voltage", False, None),
    Field(594, "B", "present_temperature", "Present Internal Temperature", False, None),
    Field(595, "B", "grip_detection", "Grip Detection", False, None),
    Field(600, "H", "external_port_data_1", "External Port Data 1", True, 0),
    Field(602, "H", "external_port_data_2", "External Port Data 2", True, 0),
    Field(604, "H", "external_port_data_3", "External Port Data 3", True, 0),
    Field(606, "H", "external_port_data_4", "External Port Data 4", True, 0)
]

RHP12RNA_RAM_FIELDS += [
    Field(634 + i, "B", "indirect_data_{}".format(i + 1), "Indirect Data {}".format(i + 1), True, 0) for i in range(128)
]

RHP12RNA_FIELDS = RHP12RNA_EEPROM_FIELDS + RHP12RNA_RAM_FIELDS


class RHP12RNAConnector(DynamixelConnector):
    def __init__(self, device: str = "/dev/ttyUSB0", baud_rate: int = 57600, dynamixel_id: int = 1):
        super(RHP12RNAConnector, self).__init__(
            RHP12RNA_FIELDS, device=device, baud_rate=baud_rate, dynamixel_id=dynamixel_id)

    def connect(self):
        super(RHP12RNAConnector, self).connect()
        model_number = self.read_field("model_number")
        if model_number != self.fields["model_number"].initial_value:
            warnings.warn("The connected device does not appear to be a RH-P12-RN(A) gripper.")
