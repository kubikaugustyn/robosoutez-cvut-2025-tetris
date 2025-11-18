#!/usr/bin/env pybricks-micropython
#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from threading import Thread

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


def main() -> None:
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


if __name__ == '__main__':
    # main()
    print("Hello World")


    def thread():
        while robot.state()[1] <= 0:
            print("Waiting...")
            wait(100)

        while robot.state()[1] > 0:
            print("Drive speed:", robot.state()[1])
            print("Distance driven:", robot.distance())
            wait(100)


    Thread(target=thread).start()
    robot.straight(1000)
