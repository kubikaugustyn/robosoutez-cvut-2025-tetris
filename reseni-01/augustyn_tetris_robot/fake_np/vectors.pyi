#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import math
from typing import Final, Self, Iterator, Iterable

Scalar = float


class Vec2:
    x: Scalar
    y: Scalar

    def __init__(self, x: Scalar, y: Scalar) -> None:
        ...

    def __add__(self, other: Self) -> Self:
        ...

    def __sub__(self, other: Self) -> Self: ...

    def __mul__(self, scalar: Scalar) -> Self: ...

    def __truediv__(self, scalar: Scalar) -> Self: ...

    def length(self) -> float: ...

    def normalized(self) -> Self: ...

    def copy_rotated(self, origin: Self, angle: float) -> Self: ...

    def __iter__(self) -> tuple[Scalar]: ...

    def __repr__(self): ...


class Vec3:
    x: Scalar
    y: Scalar
    z: Scalar

    def __init__(self, x: Scalar, y: Scalar, z: Scalar): ...

    def __iter__(self) -> Iterator[Scalar]: ...

    def __repr__(self): ...


# R, G, B as 0...1
"""class Color(Vec3):
    def as_ansi_bg_color(self) -> str: ...

    def ansi_bg_colorize(self, text: str) -> str: ...

    def distance(self, other: Vec3) -> Vec3: ...

    def distance_fast(self, other: Vec3) -> Scalar: ...

    def distance_tuple(self, other: Vec3) -> tuple[Scalar, Scalar, Scalar]: ...

    def rel_distance(self, other: Vec3, maximum_distance: Vec3) -> Vec3: ..."""


class Color:
    x: float
    y: float
    z: float

    def __init__(self, r: float, g: float, b: float) -> None: ...

    def as_ansi_bg_color(self) -> str: ...

    def ansi_bg_colorize(self, text: str) -> str: ...

    def distance_tuple(self, other: Self) -> tuple[float, float, float]: ...

    def distance_sum(self, other: Self) -> float: ...

    def distance_max(self, other: Self) -> float: ...

    def rel_distance_tuple(self, other: Self, maximum_distance: tuple[float, float, float]) -> \
            tuple[float, float, float]: ...

    def rel_distance_avg(self, other: Self, maximum_distance: Self) -> float: ...

    def is_similar(self, other: Self, threshold: float) -> bool: ...

    def channel_with_max_diff(self, other: Self) -> int: ...

    def __iter__(self) -> Iterator[float]: ...

    def __repr__(self) -> str: ...


class Colors:
    RED: Final[Color]
    GREEN: Final[Color]
    BLUE: Final[Color]
    CYAN: Final[Color]
    MAGENTA: Final[Color]
    YELLOW: Final[Color]
    WHITE: Final[Color]
    BLACK: Final[Color]
