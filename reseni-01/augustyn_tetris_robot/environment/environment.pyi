#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from typing import Self

from augustyn_tetris_robot.environment.objects import EnvironmentObject, Robot


class Environment:
    simulation: bool
    objects: list[EnvironmentObject]
    robot: Robot

    def __init__(self, simulation: bool, objects: list[EnvironmentObject], robot: Robot) -> None:
        ...

    @classmethod
    def normal(cls, *, simulation: bool) -> Self: ...
