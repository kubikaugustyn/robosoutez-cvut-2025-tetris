#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import numpy as np
import cv2
from cv2.typing import MatLike

from augustyn_tetris_robot.fake_np.polygons import AbstractPolygon
from augustyn_tetris_robot.fake_np.vectors import Color


def _color_to_cv2(color: Color) -> tuple[int, int, int]:
    c_norm = lambda channel: min(max(int(channel * 255), 0), 255)
    return c_norm(color.x), c_norm(color.y), c_norm(color.z)


def _poly_to_cv2(poly: AbstractPolygon) -> list[np.ndarray]:
    return [
        np.array(
            [[int(vertex.x), int(vertex.y)] for vertex in sub_poly.vertices()],
            dtype=np.int32
        )
        for sub_poly in poly.polygons()
    ]


def polylines(img: MatLike, poly: AbstractPolygon, isClosed: bool, color: Color,
              thickness: int | None = None, lineType: int | None = None,
              shift: int | None = None) -> MatLike:
    return cv2.polylines(
        img,
        _poly_to_cv2(poly),
        isClosed,
        _color_to_cv2(color),
        thickness,
        lineType, shift
    )


def fillPoly(img: cv2.typing.MatLike, poly: AbstractPolygon, color: Color,
             lineType: int | None = None, shift: int | None = None,
             offset: cv2.typing.Point | None = None) -> cv2.typing.MatLike:
    return cv2.fillPoly(
        img,
        _poly_to_cv2(poly),
        _color_to_cv2(color),
        lineType, shift, offset
    )
