#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from typing import Self

from augustyn_tetris_robot.fake_np.vectors import Vec2, Scalar


def _ccw(p1: Vec2, p2: Vec2, p3: Vec2) -> bool:
    """Vrátí True, pokud body p1, p2, p3 jsou proti směru hodinových ručiček"""
    ...


def _segments_intersect(a1: Vec2, b1: Vec2, a2: Vec2, b2: Vec2) -> bool:
    """Zjistí, jestli se protínají úsečky a1-b1 a a2-b2"""
    ...


class AbstractPolygon:
    _translation: Vec2

    def __init__(self, translation: Vec2 | None = None) -> None:
        ...

    def vertices(self) -> list[Vec2]:
        ...

    def polygons(self) -> list[Self]:
        ...

    def edges(self) -> list[tuple[Vec2, Vec2]]:
        ...

    def bbox(self) -> "Rectangle":
        ...

    def translated(self, translation: Vec2) -> Self:
        ...

    def intersects(self, other: Self, *, checkBBoxes: bool = False,
                   checkEdges: bool = False) -> bool:
        ...

    def centroid(self) -> Vec2:
        ...

    def penetration_depth(self, other: Self) -> float: ...

    def copy_rotated(self, origin: Vec2, angle: float) -> "MultiPolygon": ...


class Polygon(AbstractPolygon):
    _vertices: list[Vec2]

    def __init__(self, vertices: list[Vec2], translation: Vec2 | None = None) -> None: ...


class MultiPolygon(AbstractPolygon):
    _polygons: list[AbstractPolygon]
    _vertices: list[Vec2] | None

    def __init__(self, polygons: list[AbstractPolygon],
                 translation: Vec2 | None = None) -> None: ...


class Line(Polygon):
    def __init__(self, start: Vec2, end: Vec2) -> None: ...

    @property
    def start(self) -> Vec2: ...

    @property
    def end(self) -> Vec2: ...


class MultiLine(MultiPolygon):
    _polygons: list[Line]

    def __init__(self, lines: list[Line], translation: Vec2 | None = None) -> None:
        ...


class Rectangle(Polygon):
    def __init__(self, top_left: Vec2, bottom_right: Vec2) -> None: ...

    @classmethod
    def from_top_left_width_height(cls, top: Scalar, left: Scalar, width: Scalar,
                                   height: Scalar) -> Self: ...

    @property
    def top_left(self) -> Vec2: ...

    @property
    def top_right(self) -> Vec2: ...

    @property
    def bottom_right(self) -> Vec2: ...

    @property
    def bottom_left(self) -> Vec2: ...
