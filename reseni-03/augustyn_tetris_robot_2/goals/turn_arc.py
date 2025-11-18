#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import math

from pybricks.tools import wait

from augustyn_tetris_robot_2.reality.brick import Brick


def turn_arc(radius: int, angle: int, compensation_delay: int = 10) -> None:
    # turn_arc(250, 360) doesn't turn far enough
    raise NotImplementedError("Too inaccurate")

    if angle == 0:
        raise ValueError("Seriously?")
    direction = 1 if angle > 0 else -1
    Brick.wheels.reset()

    while direction * (angle - Brick.wheels.angle()) > 0:
        # angular velocity = omega * radius
        # --> omega = angular velocity / radius
        missing_angle = direction * (angle - Brick.wheels.angle())
        print("Missing angle:", missing_angle, "deg")
        speed = Brick.DRIVE_SPEED
        if missing_angle < 10:
            speed *= 0.5
        Brick.wheels.drive(speed, direction * math.degrees(speed / radius))

        Brick.may_shutdown()
        wait(compensation_delay)

    Brick.wheels.stop()
