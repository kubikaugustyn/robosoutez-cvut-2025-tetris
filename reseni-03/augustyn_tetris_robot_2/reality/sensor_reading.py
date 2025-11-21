#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import math

from augustyn_tetris_robot.environment.sensors import SensorReading
from augustyn_tetris_robot.fake_np.vectors import Color
from augustyn_tetris_robot.reality.brick import Brick


def get_real_sensor_reading(calibration):
    r, g, b = Brick.color_sensor.rgb()
    color_sensor_color = Color(r / 100, g / 100, b / 100)
    return SensorReading(
        math.radians(Brick.wheels.angle()),
        Brick.wheels.distance(),
        math.radians(Brick.left_wheel.angle()),
        math.radians(Brick.right_wheel.angle()),
        math.radians(Brick.part_pusher.angle()),
        calibration.calibrated_color_sensor_color(color_sensor_color),
        Brick.distance_sensor.distance()
    )
