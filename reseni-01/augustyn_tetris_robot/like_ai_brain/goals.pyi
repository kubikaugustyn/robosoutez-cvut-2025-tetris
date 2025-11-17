#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from collections.abc import Callable
from typing import Self, Final

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.environment.sensors import SensorReading, Calibration
from augustyn_tetris_robot.like_ai_brain.goal import Goal


class Goals:
    _GOALS: dict[str, type[Self]] = ...

    name: str
    goals: list[Goal]
    current_goal: int

    def __init__(self, name: str, calibration: Calibration) -> None: ...

    @classmethod
    def factory(cls, name: str) -> Callable[[Calibration], Self]: ...

    @classmethod
    def register(cls, name: str) -> Callable[[type[Self]], type[Self]]: ...

    @classmethod
    def get_all_goals(cls, calibration: Calibration) -> list[Goal]: ...

    def step(self, environment: Environment, sensors: SensorReading,
             sensor_diff: SensorReading) -> bool: ...


GOALS_ABYSS: Final[Callable[[Calibration], Goals]]


def get_current_goals(calibration: Calibration) -> Goals: ...
