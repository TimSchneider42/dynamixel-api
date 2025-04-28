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

from typing import Union, Any


class Motor:
    def __init__(self, connector):
        self.__connector = connector

    def __to_rel(self, value, min, max):
        return (value - min) / (max - min)

    def __to_abs(self, value, min, max):
        return value * (max - min) + min
    
    @property
    def connector(self):
        return self.__connector

    @property
    def operating_mode(self):
        return self.__connector.read_field("operating_mode")

    @operating_mode.setter
    def operating_mode(self, value: int):
        self.__connector.write_field("operating_mode", value)

    @property
    def position_limit_low(self):
        return self.__connector.read_field("min_position_limit")

    @property
    def position_limit_high(self):
        return self.__connector.read_field("max_position_limit")

    @position_limit_low.setter
    def position_limit_low(self, value: int):
        self.__connector.write_field("min_position_limit", value)

    @position_limit_high.setter
    def position_limit_high(self, value: int):
        self.__connector.write_field("max_position_limit", value)

    @property
    def velocity_limit(self):
        return self.__connector.read_field("velocity_limit")

    @velocity_limit.setter
    def velocity_limit(self, value: int):
        self.__connector.write_field("velocity_limit", value)

    @property
    def acceleration_limit(self):
        return self.__connector.read_field("acceleration_limit")

    @acceleration_limit.setter
    def acceleration_limit(self, value: int):
        self.__connector.write_field("acceleration_limit", value)

    @property
    def pwm_limit(self):
        return self.__connector.read_field("pwm_limit")

    @pwm_limit.setter
    def pwm_limit(self, value: int):
        self.__connector.write_field("pwm_limit", value)

    @property
    def torque_enabled(self):
        return self.__connector.read_field("torque_enable")

    @torque_enabled.setter
    def torque_enabled(self, value: bool):
        self.__connector.write_field("torque_enable", value)

    @property
    def current_position(self):
        return self.__connector.read_field("present_position")

    @property
    def current_position_rel(self):
        return self.__to_rel(self.current_position, self.position_limit_low, self.position_limit_high)

    @property
    def current_velocity(self):
        return self.__connector.read_field("present_velocity")

    @property
    def current_velocity_rel(self):
        return self.__to_rel(self.current_velocity, 0, self.velocity_limit)

    @property
    def goal_position(self):
        return self.__connector.read_field("goal_position")

    @goal_position.setter
    def goal_position(self, value: int):
        self.__connector.write_field("goal_position", value)

    @property
    def goal_position_rel(self):
        return self.__to_rel(self.goal_position, self.position_limit_low, self.position_limit_high)

    @goal_position_rel.setter
    def goal_position_rel(self, value: float):
        self.goal_position = int(round(self.__to_abs(value, self.position_limit_low, self.position_limit_high)))

    @property
    def goal_velocity(self):
        return self.__connector.read_field("goal_velocity")

    @goal_velocity.setter
    def goal_velocity(self, value: int):
        self.__connector.write_field("goal_velocity", value)

    @property
    def goal_velocity_rel(self):
        return self.__to_rel(self.goal_velocity, 0, self.velocity_limit)

    @goal_velocity_rel.setter
    def goal_velocity_rel(self, value: float):
        self.goal_velocity = int(round(self.__to_abs(value, 0, self.velocity_limit)))

    @property
    def goal_acceleration(self):
        return self.__connector.read_field("goal_acceleration")

    @goal_acceleration.setter
    def goal_acceleration(self, value: int):
        self.__connector.write_field("goal_acceleration", value)

    @property
    def goal_acceleration_rel(self):
        return self.__to_rel(self.goal_acceleration, 0, self.acceleration_limit)

    @goal_acceleration_rel.setter
    def goal_acceleration_rel(self, value: float):
        self.goal_acceleration = int(round(self.__to_abs(value, 0, self.acceleration_limit)))

    @property
    def goal_pwm(self):
        return self.__connector.read_field("goal_pwm")

    @goal_pwm.setter
    def goal_pwm(self, value: int):
        self.__connector.write_field("goal_pwm", value)

    @property
    def goal_pwm_rel(self):
        return self.__to_rel(self.goal_pwm, -self.pwm_limit, self.pwm_limit)

    @goal_pwm_rel.setter
    def goal_pwm_rel(self, value: float):
        self.goal_pwm = int(round(self.__to_abs(value, -self.pwm_limit, self.pwm_limit)))
