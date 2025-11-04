#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import numpy as np
import cv2
from cv2.typing import MatLike

from augustyn_tetris_robot.environment.environment import Environment
import augustyn_tetris_robot.simulation.drawing as drawing
from augustyn_tetris_robot.environment.objects import EnvironmentObject
from augustyn_tetris_robot.fake_np.vectors import Vec2, Colors


def _render_object(img: MatLike, obj: EnvironmentObject) -> None:
    if obj.stroke is not None:
        drawing.polylines(img, obj.geom, False, obj.stroke_color, int(obj.stroke))
    if obj.fill is not None:
        drawing.fillPoly(img, obj.geom, obj.fill)

    if obj.type_ == EnvironmentObject.TYPE_BLOCK:
        for vertex in obj.geom.vertices():
            cv2.circle(img, (int(vertex.x), int(vertex.y)), 2, (0, 0, 255), -1)
        centroid: Vec2 = obj.geom.centroid()
        cv2.circle(img, (int(centroid.x), int(centroid.y)), 3, (255, 0, 0), -1)

    # for edge in obj.geom.edges():
    #     cv2.line(img, (int(edge[0].x), int(edge[0].y)), (int(edge[1].x), int(edge[1].y)),
    #              (0, 0, 255), 2)


def render(environment: Environment) -> MatLike:
    img: MatLike = np.ones((1720, 1280, 3), dtype=np.uint8) * 255
    translation: Vec2 = Vec2(10, 20)

    for obj in environment.objects:
        _render_object(img, obj.translated(translation))

    _render_object(img, environment.robot.as_object().translated(translation))

    return img
