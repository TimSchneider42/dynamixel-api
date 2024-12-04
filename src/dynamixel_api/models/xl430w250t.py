"""
MIT License

Copyright (c) 2021 Tim Schneider
Copyright (c) 2024 Erik Helmut

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

XL430W250T_EEPROM_FIELDS = [
    Field(0, "H", "model_number", "Model Number", False, 1060),
    Field(2, "i", "model_information", "Model Information", False, None),
    Field(6, "B", "firmware_version", "Firmware Version", False, None),
    Field(7, "B", "id", "DYNAMIXEL ID", True, 1),
    Field(8, "B", "baud_rate", "Communication Speed", True, 1),
    Field(9, "B", "return_delay_time", "Response Delay Time", True, 250),
    Field(10, "B", "drive_mode", "Drive Mode", True, 0),
    Field(11, "B", "operating_mode", "Operating Mode", True, 3),
    Field(12, "B", "secondary_id", "Secondary(Shadow) ID", True, 255),
    Field(13, "B", "protocol_type", "Protocol Type", True, 2),
    Field(20, "i", "homing_offset", "Home Offset Value", True, 0),
    Field(24, "i", "moving_threshold", "Velocity Threshold for Movement Detection", True, 10),
    Field(31, "B", "temperature_limit", "Maximum Internal Temperature Limit", True, 72),
    Field(32, "H", "max_voltage_limit", "Maximum Input Voltage Limit", True, 140),
    Field(34, "H", "min_voltage_limit", "Minimum Input Voltage Limit", True, 60),
    Field(36, "H", "pwm_limit", "PWM Limit", True, 885),
    Field(44, "i", "velocity_limit", "Maximum Velocity Limit", True, 265),
    Field(48, "i", "max_position_limit", "Maximum Position Limit", True, 4095),
    Field(52, "i", "min_position_limit", "Minimum Position Limit", True, 0),
    Field(60, "B", "startup_configuration", "Startup Configuration", True, 3),
    Field(63, "B", "shutdown", "Shutdown Error Information", True, 52)
]

XL430W250T_RAM_FIELDS = [
    Field(64, "B", "torque_enable", "Motor Torque On/Off", True, 0),
    Field(65, "B", "led", "LED", True, 0),
    Field(68, "B", "status_return_level", "Select Types of Status Return", True, 2),
    Field(69, "B", "registered_instruction", "Check Reception of Instruction", False, 0),
    Field(70, "B", "hardware_error_status", "Hardware Error Status", False, 0),
    Field(76, "H", "velocity_i_gain", "I Gain of Velocity", True, 1000),
    Field(78, "H", "velocity_p_gain", "P Gain of Velocity", True, 100),
    Field(80, "H", "position_d_gain", "D Gain of Position", True, 4000),
    Field(82, "H", "position_i_gain", "I Gain of Position", True, 0),
    Field(84, "H", "position_p_gain", "P Gain of Position", True, 640),
    Field(88, "H", "feedforward_2nd_gain", "2nd Feed-Forward Gain", True, 0),
    Field(90, "H", "feedforward_1st_gain", "1st Feed-Forward Gain", True, 0),
    Field(98, "B", "bus_watchdog", "Bus Watchdog", True, 0),
    Field(100, "h", "goal_pwm", "Target PWM Value", True, None),
    Field(104, "i", "goal_velocity", "Target Velocity Value", True, None),
    Field(108, "i", "profile_acceleration", "Profile Acceleration Value", True, 0),
    Field(112, "i", "profile_velocity", "Profile Velocity Value", True, 0),
    Field(116, "i", "goal_position", "Target Position Value", True, None),
    Field(120, "H", "realtime_tick", "System Clock", False, None),
    Field(122, "B", "moving", "Movement Status", False, 0),
    Field(123, "B", "moving_status", "Detailed Information of Movement Status", False, 0),
    Field(124, "H", "present_pwm", "Present PWM Value", False, None),
    Field(126, "h", "present_load", "Present Load Value", False, None),
    Field(128, "i", "present_velocity", "Present Velocity Value", False, None),
    Field(132, "i", "present_position", "Present Position Value", False, None),
    Field(136, "i", "velocity_trajectory", "Velocity Trajectory", False, None),
    Field(140, "i", "position_trajectory", "Position Trajectory", False, None),
    Field(144, "H", "present_input_voltage", "Present Input Voltage", False, None),
    Field(146, "B", "present_temperature", "Present Internal Temperature", False, None),
    Field(147, "B", "backup_ready", "Backup Ready", False, 0),
]

XL430W250T_RAM_FIELDS += [
    Field(168 + i * 2, "H", "indirect_address_{}".format(i + 1), "Indirect Address {}".format(i + 1), True, 224 + i) for i in range(28)
]

XL430W250T_RAM_FIELDS += [
    Field(224 + i, "B", "indirect_data_{}".format(i + 1), "Indirect Data {}".format(i + 1), True, 0) for i in range(28)
]

XL430W250T_RAM_FIELDS += [
    Field(578 + i * 2, "H", "indirect_address_{}".format(i + 29), "Indirect Address {}".format(i + 29), True, 634 + i) for i in range(28)
]

XL430W250T_RAM_FIELDS += [
    Field(634 + i, "B", "indirect_data_{}".format(i + 29), "Indirect Data {}".format(i + 29), True, 0) for i in range(28)
]

XL430W250T_FIELDS = XL430W250T_EEPROM_FIELDS + XL430W250T_RAM_FIELDS


class XL430W250TConnector(DynamixelConnector):
    def __init__(self, device: str = "/dev/ttyUSB0", baud_rate: int = 57600, dynamixel_id: int = 1):
        super(XL430W250TConnector, self).__init__(
            XL430W250T_FIELDS, device=device, baud_rate=baud_rate, dynamixel_id=dynamixel_id)

    def connect(self):
        super(XL430W250TConnector, self).connect()
        model_number = self.read_field("model_number")
        if model_number != self.fields["model_number"].initial_value:
            warnings.warn("The connected device does not appear to be a Dynamixel XL430-W250-T motor.")
