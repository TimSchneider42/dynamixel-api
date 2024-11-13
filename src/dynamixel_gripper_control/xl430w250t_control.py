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

from typing import Any

from .model.xl430w250t import XL430W250TConnector

class XL430W250T:
    def __init__(self, connector: XL430W250TConnector):
        self.__connector = connector

    def __read(self, field_name: str):
        return self.__connector.read_field(field_name)

    def __write(self, field_name: str, value: Any):
        self.__connector.write_field(field_name, int(value))

    def __to_rel(self, value, min, max):
        return (value - min) / (max - min)

    def __to_abs(self, value, min, max):
        return value * (max - min) + min
    
    @property
    def operating_mode(self):
        return self.__read("operating_mode")
    
    @operating_mode.setter
    def operating_mode(self, value: int):
        self.__write("operating_mode", value)

    @property
    def position_limit_low(self):
        return self.__read("min_position_limit")

    @property
    def position_limit_high(self):
        return self.__read("max_position_limit")

    @position_limit_low.setter
    def position_limit_low(self, value: int):
        self.__write("min_position_limit", value)

    @position_limit_high.setter
    def position_limit_high(self, value: int):
        self.__write("max_position_limit", value)

    @property
    def velocity_limit(self):
        return self.__read("velocity_limit")

    @velocity_limit.setter
    def velocity_limit(self, value: int):
        self.__write("velocity_limit", value)

    @property
    def torque_enabled(self):
        return self.__read("torque_enable")

    @torque_enabled.setter
    def torque_enabled(self, value: bool):
        self.__write("torque_enable", value)

    @property
    def current_position(self):
        return self.__read("present_position")

    @property
    def current_position_rel(self):
        return self.__to_rel(self.current_position, self.position_limit_low, self.position_limit_high)

    @property
    def current_velocity(self):
        return self.__read("present_position")

    @property
    def current_velocity_rel(self):
        vel_lim = self.velocity_limit
        return self.__to_rel(self.current_position, -vel_lim, vel_lim)

    @property
    def goal_position(self):
        return self.__read("goal_position")

    @goal_position.setter
    def goal_position(self, value: int):
        self.__write("goal_position", value)

    @property
    def goal_position_rel(self):
        return self.__to_rel(self.goal_position, self.position_limit_low, self.position_limit_high)

    @goal_position_rel.setter
    def goal_position_rel(self, value: float):
        self.goal_position = int(round(self.__to_abs(value, self.position_limit_low, self.position_limit_high)))

    @property
    def goal_velocity(self):
        return self.__read("goal_velocity")

    @goal_velocity.setter
    def goal_velocity(self, value: int):
        self.__write("goal_velocity", value)

    @property
    def goal_velocity_rel(self):
        return self.__to_rel(self.goal_velocity, -self.velocity_limit, self.velocity_limit)

    @goal_velocity_rel.setter
    def goal_velocity_rel(self, value: float):
        self.goal_velocity = int(round(self.__to_abs(value, -self.velocity_limit, self.velocity_limit)))