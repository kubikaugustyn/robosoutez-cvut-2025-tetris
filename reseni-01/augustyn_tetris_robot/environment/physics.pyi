#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from typing import Final

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.environment.sensors import SensorReading
from augustyn_tetris_robot.fake_np.vectors import Vec2

_WITH_HITBOX: Final[tuple[int, ...]] = ...
_FRICTION: Final[dict[int, float]] = ...
_SPEED_FACTOR: Final[dict[int, float]] = ...
_MIN_MOVEMENT_THRESHOLD: Final[float] = ...
_ROTATION_FACTOR: Final[float] = ...


def step(environment: Environment, sensors: SensorReading, sensor_diff: SensorReading) -> None: ...


def resolve_collisions(environment: Environment) -> None: ...


def rotate_wheels(origin: Vec2, wheels: tuple[Vec2, Vec2], angles: tuple[float, float],
                  diameters: tuple[float, float]) -> tuple[Vec2, float]:
    """
    Simulates the two wheels rotating by certain angles (in radians).

    Returns the delta of the entire robot's position and the delta of its rotation around the origin.

    Author: ČetDžíPíTý ofc
    """
    ...
