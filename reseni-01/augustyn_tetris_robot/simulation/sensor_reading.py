#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.environment.sensors import SensorReading
from augustyn_tetris_robot.fake_np.vectors import Color


def get_simulation_sensor_reading(environment: Environment) -> SensorReading:
    return SensorReading(
        0, 0,
        0, 0, 0,
        Color(0, 0, 0),
        0
    )
