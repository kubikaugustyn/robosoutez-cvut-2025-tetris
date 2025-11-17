#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Direction
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor
from pybricks.robotics import DriveBase


class Brick:
    ev3 = EV3Brick()
    left_wheel = Motor(port=Port.B, positive_direction=Direction.COUNTERCLOCKWISE)  # Ideal +-5deg
    right_wheel = Motor(port=Port.D, positive_direction=Direction.COUNTERCLOCKWISE)  # Ideal +-5deg
    # Ideal values are 56 and 184
    wheels = DriveBase(left_wheel, right_wheel, wheel_diameter=54.8, axle_track=180)
    part_pusher = Motor(port=Port.A)  # Ideal +-10deg
    color_sensor = ColorSensor(port=Port.S2)
    distance_sensor = UltrasonicSensor(port=Port.S1)

    wheels.distance_control.target_tolerances(speed=None, position=1)
    wheels.heading_control.target_tolerances(speed=None, position=1)
