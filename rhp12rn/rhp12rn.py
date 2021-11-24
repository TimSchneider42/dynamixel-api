from typing import Union, Any

from .rhp12rna_connector import RHP12RNAConnector
from .rhp12rn_connector import RHP12RNConnector


class RHP12RN:
    def __init__(self, connector: Union[RHP12RNConnector, RHP12RNAConnector]):
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
    def acceleration_limit(self):
        return self.__read("acceleration_limit")

    @acceleration_limit.setter
    def acceleration_limit(self, value: int):
        self.__write("acceleration_limit", value)

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

    @property
    def goal_acceleration(self):
        return self.__read("goal_acceleration")

    @goal_acceleration.setter
    def goal_acceleration(self, value: int):
        self.__write("goal_acceleration", value)

    @property
    def goal_acceleration_rel(self):
        return self.__to_rel(self.goal_acceleration, -self.acceleration_limit, self.acceleration_limit)

    @goal_acceleration_rel.setter
    def goal_acceleration_rel(self, value: float):
        self.goal_acceleration = int(round(self.__to_abs(value, -self.acceleration_limit, self.acceleration_limit)))
