#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from augustyn_tetris_robot.environment.sensors import Calibration
from augustyn_tetris_robot.fake_np.vectors import Color

CALIBRATION_OFF = 0
CALIBRATION_HOME = 1
CALIBRATION_DESK = 2

# CALIBRATION = CALIBRATION_OFF
CALIBRATION = CALIBRATION_HOME
# CALIBRATION = CALIBRATION_DESK


def get_real_calibration():
    calibration = Calibration()

    if CALIBRATION == CALIBRATION_OFF:
        print("Warning: not using calibration")
        calibration.color_black = Color(0, 0, 0)
        calibration.color_white = Color(1, 1, 1)
        calibration.color_line_yellow = Color(1, 1, 0)
    elif CALIBRATION == CALIBRATION_HOME:
        calibration.color_black = Color(15 / 255, 22 / 255, 50 / 255)
        calibration.color_white = Color(170 / 255, 193 / 255, 1)
        # calibration.color_line_yellow = Color(...)
    elif CALIBRATION == CALIBRATION_DESK:
        calibration.color_black = Color(0.075, 0.066, 0.105)
        calibration.color_white = Color(0.665, 0.755, 1.000)
        calibration.color_line_yellow = Color(1, 242 / 255, 195 / 255)
    else:
        raise ValueError("Unknown calibration")

    return calibration
