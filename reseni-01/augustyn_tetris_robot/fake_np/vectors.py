#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import math

Scalar = float


class Vec2:
    x: Scalar
    y: Scalar

    def __init__(self, x: Scalar, y: Scalar) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: Scalar) -> "Vec2":
        return Vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: Scalar) -> "Vec2":
        return Vec2(self.x / scalar, self.y / scalar)

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def normalized(self) -> "Vec2":
        l = self.length()
        if l == 0:
            return Vec2(0, 0)  # aby se to nerozpadlo při nulovém vektoru
        return self / l

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"


class Vec3:
    x: Scalar
    y: Scalar
    z: Scalar

    def __init__(self, x: Scalar, y: Scalar, z: Scalar):
        self.x = x
        self.y = y
        self.z = z


# R, G, B as 0...1
Color = Vec3


class Colors:
    RED = Color(1, 0, 0)
    GREEN = Color(0, 1, 0)
    BLUE = Color(0, 0, 1)
    CYAN = Color(0, 1, 1)
    MAGENTA = Color(1, 0, 1)
    YELLOW = Color(1, 1, 0)
    WHITE = Color(1, 1, 1)
    BLACK = Color(0, 0, 0)
