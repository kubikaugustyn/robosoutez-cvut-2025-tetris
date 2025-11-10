#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor


class Brick:
    ev3: EV3Brick = EV3Brick()
    left_wheel: Motor = Motor(port=Port.A, reset_angle=False, profile=5)
    right_wheel: Motor = Motor(port=Port.D, reset_angle=False, profile=5)
    part_pusher: Motor = Motor(port=Port.B, reset_angle=False, profile=10)
    color_sensor: ColorSensor = ColorSensor(port=Port.S2)
    distance_sensor: UltrasonicSensor = UltrasonicSensor(port=Port.S1)
