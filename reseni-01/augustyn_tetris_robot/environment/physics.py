#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import math
import random

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.environment.objects import EnvironmentObject
from augustyn_tetris_robot.fake_np.vectors import Vec2, Colors

_WITH_HITBOX: tuple[int, ...] = (EnvironmentObject.TYPE_WALL, EnvironmentObject.TYPE_BLOCK,
                                 EnvironmentObject.TYPE_ROBOT)
_FRICTION: dict[int, float] = {
    EnvironmentObject.TYPE_WALL: float("inf"),
    EnvironmentObject.TYPE_BLOCK: 0.1,
    EnvironmentObject.TYPE_ROBOT: 0.9,
}
_SPEED_FACTOR: dict[int, float] = {
    EnvironmentObject.TYPE_WALL: 0.1,
    EnvironmentObject.TYPE_BLOCK: 0.01,
    EnvironmentObject.TYPE_ROBOT: 0.01,
}
_MIN_MOVEMENT_THRESHOLD: float = 0.5
_ROTATION_FACTOR: float = 0.01


def step(environment: Environment) -> None:
    resolve_collisions(environment)


"""def resolve_collisions(environment: Environment) -> None:
    robot_object: EnvironmentObject = environment.robot.as_object()
    objects: list[EnvironmentObject] = [*environment.objects, robot_object]
    objects = list(filter(lambda o: o.type_ in _WITH_HITBOX, objects))

    for obj in objects:
        translation = Vec2(0, 0)
        friction = _FRICTION[obj.type_]
        if math.isinf(friction):
            continue  # objekt se nehýbe vůbec

        for other in objects:
            if obj is other:
                continue
            check_edges: bool = obj.fill is None or other.fill is None
            if obj.geom.intersects(other.geom, checkBBoxes=not check_edges, checkEdges=check_edges):
                push_vec = (obj.geom.centroid() - other.geom.centroid()).normalized()
                depth = obj.geom.penetration_depth(other.geom)
                random_factor = random.randint(10000, 10500) / 10000
                translation += push_vec * depth * _SPEED_FACTOR * random_factor / friction
                if 0 < translation.length() < _MIN_MOVEMENT_THRESHOLD:
                    translation = translation.normalized() * _MIN_MOVEMENT_THRESHOLD
        if obj is robot_object:
            environment.robot.translation += translation
        else:
            obj.geom = obj.geom.translated(translation)"""


def resolve_collisions(environment: Environment) -> None:
    robot_object: EnvironmentObject = environment.robot.as_object()
    objects: list[EnvironmentObject] = [*environment.objects, robot_object]
    objects = list(filter(lambda o: o.type_ in _WITH_HITBOX, objects))

    for obj in objects:
        translation = Vec2(0, 0)
        rotation_angle = 0.0
        friction = _FRICTION[obj.type_]
        if math.isinf(friction):
            continue  # objekt se nehýbe vůbec

        for other in objects:
            if obj is other:
                continue
            check_edges: bool = obj.fill is None or other.fill is None
            if obj.geom.intersects(other.geom, checkBBoxes=not check_edges, checkEdges=check_edges):
                push_vec: Vec2 = (obj.geom.centroid() - other.geom.centroid()).normalized()
                depth = obj.geom.penetration_depth(other.geom)
                random_factor = random.randint(10000, 10500) / 10000
                k: float = depth * _SPEED_FACTOR[other.type_] * random_factor / friction
                translation += push_vec * k

                # Rotace
                lever: float = (obj.geom.centroid() - other.geom.centroid()).length()
                torque = depth * _ROTATION_FACTOR / (friction * max(lever, 1e-6))
                direction = 1 if random.random() > 0.5 else -1  # náhodně doleva/doprava
                rotation_angle += torque * direction

        if 0.0 < translation.length() < _MIN_MOVEMENT_THRESHOLD:
            translation = translation.normalized() * _MIN_MOVEMENT_THRESHOLD

        if obj is robot_object:
            environment.robot.translation += translation
            environment.robot.rotation += rotation_angle
        else:
            obj.geom = obj.geom.translated(translation)
            if rotation_angle != 0:
                obj.geom = obj.geom.copy_rotated(obj.geom.centroid(), rotation_angle)
