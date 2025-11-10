#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.fake_np.vectors import Scalar, Color


class SensorReading:
    # Angles in radians
    left_wheel_angle: float
    right_wheel_angle: float
    part_pusher_angle: float
    color_sensor_color: Color
    distance_sensor_distance: Scalar

    def __init__(self, left_wheel_angle: float, right_wheel_angle: float, part_pusher_angle: float,
                 color_sensor_color: Color, distance_sensor_distance: Scalar) -> None:
        self.left_wheel_angle = left_wheel_angle
        self.right_wheel_angle = right_wheel_angle
        self.part_pusher_angle = part_pusher_angle
        self.color_sensor_color = color_sensor_color
        self.distance_sensor_distance = distance_sensor_distance

    def difference(self, previous: "SensorReading") -> "SensorReading":
        return SensorReading(
            self.left_wheel_angle - previous.left_wheel_angle,
            self.right_wheel_angle - previous.right_wheel_angle,
            self.part_pusher_angle - self.part_pusher_angle,
            self.color_sensor_color,  # Don't subtract
            self.distance_sensor_distance - self.distance_sensor_distance
        )


def get_sensor_reading(environment: Environment) -> SensorReading:
    if environment.simulation:
        from augustyn_tetris_robot.simulation.sensor_reading import get_simulation_sensor_reading
        return get_simulation_sensor_reading()
    else:
        from augustyn_tetris_robot.reality.sensor_reading import get_real_sensor_reading
        return get_real_sensor_reading()
