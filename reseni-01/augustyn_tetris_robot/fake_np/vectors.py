#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import math

from augustyn_tetris_robot.fake_np.utils import util_map


class Vec2:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vec2(self.x / scalar, self.y / scalar)

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self):
        l = self.length()
        if l == 0:
            return Vec2(0, 0)  # aby se to nerozpadlo při nulovém vektoru
        return self / l

    def copy_rotated(self, origin, angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        # Posunout do souřadnic kolem originu
        dx = self.x - origin.x
        dy = self.y - origin.y

        # Otočit a znovu přičíst origin
        new_x = origin.x + dx * cos_a - dy * sin_a
        new_y = origin.y + dx * sin_a + dy * cos_a
        return Vec2(new_x, new_y)

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return "Vec2({:.3f}, {:.3f})".format(self.x, self.y)


class Vec3:
    __slots__ = ("x", "y", "z")

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __repr__(self):
        return "Vec3({:.3f}, {:.3f}, {:.3f})".format(self.x, self.y, self.z)


# R, G, B as 0...1
"""class Color(Vec3):
    def as_ansi_bg_color(self):
        return "\033[48;2;{};{};{}m".format(int(self.x * 255), int(self.y * 255), int(self.z * 255))

    def ansi_bg_colorize(self, text):
        return "{}{}\033[0m".format(self.as_ansi_bg_color(), text)

    def distance(self, other):
        return Vec3(
            abs(self.x - other.x),
            abs(self.y - other.y),
            abs(self.z - other.z),
        )

    def distance_fast(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def distance_tuple(self, other):
        return (
            abs(self.x - other.x),
            abs(self.y - other.y),
            abs(self.z - other.z),
        )

    def rel_distance(self, other, maximum_distance):
        distance = self.distance(other)  # TODO Maybe optimize this?
        return Vec3(
            util_map(distance.x, 0, maximum_distance.x, 0, 1, limit=True),
            util_map(distance.y, 0, maximum_distance.y, 0, 1, limit=True),
            util_map(distance.z, 0, maximum_distance.z, 0, 1, limit=True),
        )"""


# Turbo Color - minimal allocations, micro-optimized for MicroPython/EV3 (By Chad)
class Color:
    __slots__ = ("x", "y", "z")

    def __init__(self, r, g, b):
        self.x = r
        self.y = g
        self.z = b

    # existing ANSI helper (ok as-is, cheap)
    def as_ansi_bg_color(self):
        # int(...) jen při výstupu, ne při každém výpočtu
        return "\033[48;2;{};{};{}m".format(int(self.x * 255), int(self.y * 255), int(self.z * 255))

    def ansi_bg_colorize(self, text):
        return "{}{}\033[0m".format(self.as_ansi_bg_color(), text)

    # --- distance variants (no object allocations) ---
    def distance_tuple(self, other):
        """Return absolute per-channel difference as tuple (dx, dy, dz)."""
        # math.fabs je obvykle rychlejší než abs na float v některých MicroPython buildech
        return (math.fabs(self.x - other.x), math.fabs(self.y - other.y),
                math.fabs(self.z - other.z))

    def distance_sum(self, other):
        """Sum of absolute differences — single scalar, zero allocations."""
        dx = math.fabs(self.x - other.x)
        dy = math.fabs(self.y - other.y)
        dz = math.fabs(self.z - other.z)
        return dx + dy + dz

    def distance_max(self, other):
        """Max channel difference — single scalar, zero allocations."""
        dx = math.fabs(self.x - other.x)
        dy = math.fabs(self.y - other.y)
        dz = math.fabs(self.z - other.z)
        # inline max to avoid tuple allocation
        m = dx if dx >= dy else dy
        return m if m >= dz else dz

    # --- relative distances mapped to 0..1 (no Vec3 allocation) ---
    def rel_distance_tuple(self, other, maximum_distance):
        """Return per-channel relative distance as a tuple of floats in [0,1]."""
        um = util_map  # local ref faster
        dx = math.fabs(self.x - other.x)
        dy = math.fabs(self.y - other.y)
        dz = math.fabs(self.z - other.z)
        return (
            um(dx, 0.0, maximum_distance[0], 0.0, 1.0, limit=True),
            um(dy, 0.0, maximum_distance[1], 0.0, 1.0, limit=True),
            um(dz, 0.0, maximum_distance[2], 0.0, 1.0, limit=True),
        )

    def rel_distance_avg(self, other, maximum_distance):
        """Average of per-channel relative distances -> single scalar [0,1]."""
        a, b, c = self.rel_distance_tuple(other, maximum_distance)
        return (a + b + c) / 3.0

    # --- ultra-fast comparison helpers (no trig, no allocation) ---
    def is_similar(self, other, threshold):
        """Quick boolean: sum of absolute diffs <= threshold."""
        return self.distance_sum(other) <= threshold

    def channel_with_max_diff(self, other):
        """Return index 0/1/2 of channel with largest absolute diff (no allocation)."""
        dx = math.fabs(self.x - other.x)
        dy = math.fabs(self.y - other.y)
        dz = math.fabs(self.z - other.z)
        if dx >= dy and dx >= dz:
            return 0
        if dy >= dz:
            return 1
        return 2

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __repr__(self):
        return "Color({:.3f}, {:.3f}, {:.3f})".format(self.x, self.y, self.z)


class Colors:
    RED = Color(1, 0, 0)
    GREEN = Color(0, 1, 0)
    BLUE = Color(0, 0, 1)
    CYAN = Color(0, 1, 1)
    MAGENTA = Color(1, 0, 1)
    YELLOW = Color(1, 1, 0)
    WHITE = Color(1, 1, 1)
    BLACK = Color(0, 0, 0)
