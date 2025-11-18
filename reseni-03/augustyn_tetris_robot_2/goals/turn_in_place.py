#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from augustyn_tetris_robot_2.reality.brick import Brick


def turn_in_place(angle: int) -> None:
    Brick.wheels.turn(angle)
    Brick.wheels.stop()
