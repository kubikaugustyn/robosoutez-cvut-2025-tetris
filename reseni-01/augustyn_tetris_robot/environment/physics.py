#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import math
import random

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.environment.objects import EnvironmentObject
from augustyn_tetris_robot.environment.sensors import SensorReading
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


def step(environment: Environment, sensors: SensorReading, sensor_diff: SensorReading) -> None:
    # Robot movement
    delta_robot_pos, delta_robot_angle = rotate_wheels(
        environment.robot.origin,
        environment.robot.wheels,
        (sensor_diff.left_wheel_angle, sensor_diff.right_wheel_angle),
        (environment.robot.wheel_diameter, environment.robot.wheel_diameter)
    )
    environment.robot.translation += delta_robot_pos
    environment.robot.rotation += delta_robot_angle

    # Robot part pusher
    # https://medium.com/kidstronics/lego-gears-worms-bf8ef3280d0e#6699
    environment.robot.part_pusher_rotation += sensor_diff.part_pusher_angle / 24  # 1:24

    # The real physics
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


def rotate_wheels(origin: Vec2, wheels: tuple[Vec2, Vec2], angles: tuple[float, float],
                  diameters: tuple[float, float]) -> tuple[Vec2, float]:
    """
    Simulates the two wheels rotating by certain angles (in radians).

    Returns the delta of the entire robot's position and the delta of its rotation around the origin.

    Author: ČetDžíPíTý ofc
    """

    s1 = angles[0] * diameters[0] / 2
    s2 = angles[1] * diameters[1] / 2
    L = (wheels[0] - wheels[1]).length()

    # rozdíl dráhy -> rotace robota
    if abs(s2 - s1) < 1e-9:
        # rovný pohyb vpřed
        forward = ((wheels[0] + wheels[1]) / 2 - origin).normalized()
        delta_pos = forward * ((s1 + s2) / 2)
        delta_angle = 0.0
    else:
        delta_angle = (s2 - s1) / L
        R = (L / 2) * (s1 + s2) / (s2 - s1)

        # posun středu robota relativně k jeho směru
        dx = math.sin(delta_angle) * R
        dy = R * (1 - math.cos(delta_angle))

        forward = ((wheels[0] + wheels[1]) / 2 - origin).normalized()
        right = Vec2(forward.y, -forward.x)

        delta_pos = forward * dy + right * dx

    return delta_pos, delta_angle
