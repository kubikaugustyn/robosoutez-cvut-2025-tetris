#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from augustyn_tetris_robot_2.utils import util_map

CALIBRATION_OFF = 0
CALIBRATION_HOME = 1
CALIBRATION_DESK = 2

# @formatter:off
# CALIBRATION = CALIBRATION_OFF
CALIBRATION = CALIBRATION_HOME
# CALIBRATION = CALIBRATION_DESK
# @formatter:on

if CALIBRATION == CALIBRATION_OFF:
    print("Warning: not using calibration")


def calibrated_color_sensor_reflection(raw):
    assert 0 <= raw <= 100
    if CALIBRATION == CALIBRATION_OFF:
        return raw
    elif CALIBRATION == CALIBRATION_HOME:
        return int(util_map(raw, 5, 77, 0, 100, True))
    elif CALIBRATION == CALIBRATION_DESK:
        return int(util_map(raw, 7, 73, 0, 100, True))
    else:
        raise ValueError("Unknown calibration")
