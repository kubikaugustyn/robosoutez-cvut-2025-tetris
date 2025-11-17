#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import math  # This is like the only micropython module

from augustyn_tetris_robot.fake_np.vectors import Vec2


def _ccw(p1, p2, p3):
    """Vrátí True, pokud body p1, p2, p3 jsou proti směru hodinových ručiček"""
    return (p3.y - p1.y) * (p2.x - p1.x) > (p2.y - p1.y) * (p3.x - p1.x)


def _segments_intersect(a1, b1, a2, b2):
    """Zjistí, jestli se protínají úsečky a1-b1 a a2-b2"""
    return _ccw(a1, a2, b2) != _ccw(b1, a2, b2) and _ccw(a1, b1, a2) != _ccw(a1, b1, b2)


class AbstractPolygon:
    def __init__(self, translation=None):
        self._translation = translation or Vec2(0, 0)

    def vertices(self):
        raise NotImplementedError("{} doesn't implement vertices()".format(type(self).__name__))

    def polygons(self):
        raise NotImplementedError("{} doesn't implement polygons()".format(type(self).__name__))

    def edges(self):
        raise NotImplementedError("{} doesn't implement edges()".format(type(self).__name__))

    def bbox(self):
        left, top, right, bottom = float("inf"), float("inf"), float("-inf"), float("-inf")
        for vertex in self.vertices():
            left = min(left, vertex.x)
            top = min(top, vertex.y)
            right = max(right, vertex.x)
            bottom = max(bottom, vertex.y)
        return Rectangle(Vec2(left, top), Vec2(right, bottom))

    def translated(self, translation):
        raise NotImplementedError("{} doesn't implement translated()".format(type(self).__name__))

    def intersects(self, other, *, checkBBoxes=False, checkEdges=False):
        if checkBBoxes:
            return self.bbox().intersects(other.bbox(), checkBBoxes=True)
        elif checkEdges:
            if not self.bbox().intersects(other.bbox(), checkBBoxes=True):
                # Skip the expensive calculations if the bounding boxes don't intersect at all
                return False

            edges1 = self.edges()
            edges2 = other.edges()
            for edge1 in edges1:
                for edge2 in edges2:
                    if _segments_intersect(edge1[0], edge1[1], edge2[0], edge2[1]):
                        return True
            return False
        else:
            raise ValueError("At least one of checkBBoxes or checkEdges must be True")

    def centroid(self):
        vertices = self.vertices()
        if not vertices:
            return Vec2(0, 0)
        x = sum(v.x for v in vertices) / len(vertices)
        y = sum(v.y for v in vertices) / len(vertices)
        return Vec2(x, y)

    def penetration_depth(self, other):
        bbox1 = self.bbox()
        bbox2 = other.bbox()
        dx = min(bbox1.bottom_right.x - bbox2.top_left.x, bbox2.bottom_right.x - bbox1.top_left.x)
        dy = min(bbox1.bottom_right.y - bbox2.top_left.y, bbox2.bottom_right.y - bbox1.top_left.y)
        return min(dx, dy)

    def copy_rotated(self, origin, angle):
        polygons = []  # list[Polygon]
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        for poly in self.polygons():
            vertices = poly.vertices().copy()  # list[Vec2]

            for vertex in vertices:
                # Posunout do souřadnic kolem originu
                dx = vertex.x - origin.x
                dy = vertex.y - origin.y

                # Otočit a znovu přičíst origin
                vertex.x = origin.x + dx * cos_a - dy * sin_a
                vertex.y = origin.y + dx * sin_a + dy * cos_a

            polygons.append(Polygon(vertices))

        return MultiPolygon(polygons)


class Polygon(AbstractPolygon):
    def __init__(self, vertices, translation=None):
        super().__init__(translation)
        self._vertices = vertices

    def vertices(self):
        return [vertex + self._translation for vertex in self._vertices]

    def polygons(self):
        return [self]

    def edges(self):
        vertices = self.vertices()  # list[Vec2]
        edges = [] # list[tuple[Vec2, Vec2]]
        for i in range(len(vertices) - 1):
            edges.append((vertices[i], vertices[i + 1]))
        return edges

    def translated(self, translation):
        return Polygon(self._vertices, self._translation + translation)


class MultiPolygon(AbstractPolygon):
    def __init__(self, polygons, translation=None) -> None:
        super().__init__(translation)
        self._polygons = polygons
        self._vertices = None

    def vertices(self):
        if self._vertices is not None:
            return self._vertices

        self._vertices = []
        for polygon in self._polygons:
            self._vertices.extend(polygon.translated(self._translation).vertices())
        return self._vertices

    def polygons(self):
        return [
            sub_poly
            for poly in self._polygons
            for sub_poly in poly.translated(self._translation).polygons()
        ]

    def edges(self):
        edges = [] # list[tuple[Vec2, Vec2]]
        for polygon in self.polygons():
            edges.extend(polygon.edges())
        return edges

    def translated(self, translation):
        return MultiPolygon(self._polygons, self._translation + translation)


class Line(Polygon):
    def __init__(self, start, end):
        super().__init__([start, end])

    @property
    def start(self):
        return self._vertices[0]

    @property
    def end(self):
        return self._vertices[1]

    def translated(self, translation):
        return Line(self.start + translation, self.end + translation)


class MultiLine(MultiPolygon):
    def __init__(self, lines, translation=None) -> None:
        super().__init__(lines, translation)

    def translated(self, translation):
        return MultiLine(self._polygons, self._translation + translation)


class Rectangle(Polygon):
    def __init__(self, top_left, bottom_right):
        super().__init__([
            # Top left, top right, bottom right, bottom left
            top_left,
            Vec2(bottom_right.x, top_left.y),
            bottom_right,
            Vec2(top_left.x, bottom_right.y),
            top_left  # Close the polygon
        ])

    @classmethod
    def from_top_left_width_height(cls, top, left, width, height):
        return cls(Vec2(left, top), Vec2(left + width, top + height))

    @property
    def top_left(self):
        return self._vertices[0]

    @property
    def top_right(self):
        return self._vertices[1]

    @property
    def bottom_right(self):
        return self._vertices[2]

    @property
    def bottom_left(self):
        return self._vertices[3]

    def translated(self, translation):
        return Rectangle(self.top_left + translation, self.bottom_right + translation)

    def intersects(self, other, *, checkBBoxes=False, checkEdges=False):
        if checkBBoxes and isinstance(other, Rectangle):
            return not (
                    self.bottom_right.x < other.top_left.x
                    or self.top_left.x > other.bottom_right.x
                    or self.bottom_right.y < other.top_left.y
                    or self.top_left.y > other.bottom_right.y
            )
        return super().intersects(other, checkBBoxes=checkBBoxes, checkEdges=checkEdges)
