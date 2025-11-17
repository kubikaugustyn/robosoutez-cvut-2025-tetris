#!/usr/bin/env pybricks-micropython
#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

"""
Example LEGO® MINDSTORMS® EV3 Robot Educator Color Sensor Down Program
----------------------------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot
"""

from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait
from pybricks.robotics import DriveBase

# Initialize the motors.
left_motor = Motor(port=Port.B, positive_direction=Direction.COUNTERCLOCKWISE)
right_motor = Motor(port=Port.D, positive_direction=Direction.COUNTERCLOCKWISE)

# Initialize the color sensor.
line_sensor = ColorSensor(Port.S2)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=54.8, axle_track=180)

# Calculate the light threshold. Choose values based on your measurements.
BLACK = 9
WHITE = 85
threshold = (BLACK + WHITE) / 2

# Set the drive speed at 100 millimeters per second.
DRIVE_SPEED = 100

# Set the gain of the proportional line controller. This means that for every
# percentage point of light deviating from the threshold, we set the turn
# rate of the drivebase to 1.2 degrees per second.

# For example, if the light value deviates from the threshold by 10, the robot
# steers at 10*1.2 = 12 degrees per second.
PROPORTIONAL_GAIN = 1.2

# Start following the line endlessly.
while True:
    # Calculate the deviation from the threshold.
    deviation = line_sensor.reflection() - threshold

    # Calculate the turn rate.
    turn_rate = PROPORTIONAL_GAIN * deviation

    # Set the drive base speed and turn rate.
    robot.drive(DRIVE_SPEED, turn_rate)

    # You can wait for a short time or do other things in this loop.
    wait(10)
