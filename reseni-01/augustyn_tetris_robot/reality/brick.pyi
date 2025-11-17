#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from typing import Final

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor
from pybricks.robotics import DriveBase


class Brick:
    ev3: Final[EV3Brick]
    left_wheel: Final[Motor]
    right_wheel: Final[Motor]
    wheels: Final[DriveBase]
    part_pusher: Final[Motor]
    color_sensor: Final[ColorSensor]
    distance_sensor: Final[UltrasonicSensor]
