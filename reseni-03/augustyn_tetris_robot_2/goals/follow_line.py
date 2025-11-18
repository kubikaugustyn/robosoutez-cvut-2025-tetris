#  -*- coding: utf-8 -*-
# Heavily inspired by https://pybricks.com/ev3-micropython/examples/robot_educator_line.html
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from pybricks.tools import wait

from augustyn_tetris_robot_2.reality.brick import Brick

# Set the gain of the proportional line controller. This means that for every
# percentage point of light deviating from the threshold, we set the turn
# rate of the drivebase to 1.2 degrees per second.

# For example, if the light value deviates from the threshold by 10, the robot
# steers at 10*1.2 = 12 degrees per second.
PROPORTIONAL_GAIN = 0.6


def follow_line_goal(distance: int, right_side: bool = False, compensation_delay: int = 10) -> None:
    Brick.wheels.reset()

    while Brick.wheels.distance() < distance:
        deviation = Brick.measure_reflection() - 50
        turn_rate = PROPORTIONAL_GAIN * Brick.SPEED * deviation
        if right_side:
            turn_rate = -turn_rate

        Brick.wheels.drive(Brick.DRIVE_SPEED, turn_rate)

        Brick.may_shutdown()
        wait(compensation_delay)

    Brick.wheels.stop()


def follow_line_backwards_goal(distance: int, right_side: bool = False,
                               compensation_delay: int = 10) -> None:
    Brick.wheels.reset()

    while Brick.wheels.distance() > -distance:
        deviation = Brick.measure_reflection() - 50
        turn_rate = PROPORTIONAL_GAIN * Brick.SPEED * deviation
        if right_side:
            turn_rate = -turn_rate

        Brick.wheels.drive(-Brick.DRIVE_SPEED, turn_rate)

        Brick.may_shutdown()
        wait(compensation_delay)

    Brick.wheels.stop()
