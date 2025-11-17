#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from typing import Self

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.fake_np.vectors import Scalar, Color


class SensorReading:
    # Angles in radians
    rotation_angle: float
    distance_driven: float
    left_wheel_angle: float
    right_wheel_angle: float
    part_pusher_angle: float
    color_sensor_color: Color
    distance_sensor_distance: Scalar

    def __init__(self, rotation_angle: float, distance_driven: float, left_wheel_angle: float,
                 right_wheel_angle: float, part_pusher_angle: float, color_sensor_color: Color,
                 distance_sensor_distance: Scalar) -> None: ...

    def difference(self, previous: Self) -> Self: ...


class Calibration:
    # Color sensor calibration
    color_black: Color
    color_white: Color
    color_line_white: Color
    color_line_black: Color
    color_line_yellow: Color

    def __init__(self) -> None: ...

    def calibrated_color_sensor_color(self, raw: Color) -> Color: ...


def get_sensor_reading(environment: Environment) -> SensorReading: ...


def get_calibration(environment: Environment) -> Calibration: ...
