#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from typing import Final, Self

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.fake_np.polygons import AbstractPolygon
from augustyn_tetris_robot.fake_np.vectors import Color, Vec2, Scalar


class EnvironmentObject:
    TYPE_WALL: Final[int]
    TYPE_BLOCK: Final[int]
    TYPE_LINE: Final[int]
    TYPE_ROBOT: Final[int]

    geom: AbstractPolygon
    type_: int
    stroke: Scalar | None
    stroke_color: Color | None
    fill: Color | None

    def __init__(self, geom: AbstractPolygon, type_: int, *, stroke: Scalar | None = None,
                 stroke_color: Color | None = None, fill: Color | None = None) -> None: ...

    def translated(self, translation: Vec2) -> Self: ...


class Block(EnvironmentObject):
    def __init__(self, geom_str: str, origin: Vec2, color: Color) -> None: ...

    @staticmethod
    def _generate_geom(geom_str: str) -> AbstractPolygon: ...

    def outline(self) -> EnvironmentObject: ...


class Blocks:
    T_NORMAL: Final[Block]
    T_UPSIDE_DOWN: Final[Block]
    L_HORIZONTAL: Final[Block]
    L_HORIZONTAL_ROTATED: Final[Block]
    S: Final[Block]
    I: Final[Block]
    O: Final[Block]


class Robot:
    rotation: float  # in radians # FIXME Use the rotation
    translation: Vec2
    translation_plus_origin: Vec2
    base_geom: AbstractPolygon

    # Moving claw
    part_pusher_rotation: float
    # Pusher, axle1, axle2
    part_pusher_starting: tuple[AbstractPolygon, AbstractPolygon, AbstractPolygon]
    part_pusher_joints: tuple[None, Vec2, Vec2]
    # Color sensor
    color_sensor: Vec2  # Origin
    # Distance sensor
    distance_sensor: tuple[Vec2, Vec2]  # Origin, direction normalized vector
    # Wheels
    wheels: tuple[Vec2, Vec2]  # Translations from the origin
    wheel_diameter: Scalar

    def __init__(self, origin: Vec2) -> None: ...

    def _generate_geom(self) -> None: ...

    def as_object(self) -> EnvironmentObject: ...

    @property
    def geom(self) -> AbstractPolygon: ...

    @property
    def part_pusher(self) -> tuple[AbstractPolygon, AbstractPolygon, AbstractPolygon]: ...
