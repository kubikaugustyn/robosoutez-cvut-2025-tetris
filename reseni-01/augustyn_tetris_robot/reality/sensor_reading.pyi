#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from augustyn_tetris_robot.environment.sensors import SensorReading, Calibration


def get_real_sensor_reading(calibration: Calibration) -> SensorReading: ...
