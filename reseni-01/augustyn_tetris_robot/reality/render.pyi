#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from typing import Final
from pybricks.media.ev3dev import Font

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.like_ai_brain.goals import Goals

tiny_font: Final[Font] = ...


class Timing:
    start_loop: float
    start_read_sensors: float
    start_physics: float
    start_goals: float
    start_render: float
    end_loop: float

    time_loop: float
    time_read_sensors: float
    time_physics: float
    time_goals: float
    time_render: float

    def __init__(self) -> None: ...

    def loop_start(self) -> None: ...

    def read_sensors(self) -> None: ...

    def physics(self) -> None: ...

    def goals(self) -> None: ...

    def render(self) -> None: ...

    def loop_end(self) -> None: ...

    def compact_time(self) -> str: ...


def render(environment: Environment, goals: Goals, timing: Timing) -> None:
    ...
