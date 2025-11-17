#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from augustyn_tetris_robot.fake_np.utils import util_map
from augustyn_tetris_robot.fake_np.vectors import Color, Colors


class SensorReading:
    def __init__(self, rotation_angle, distance_driven, left_wheel_angle, right_wheel_angle,
                 part_pusher_angle, color_sensor_color, distance_sensor_distance):
        self.rotation_angle = rotation_angle
        self.distance_driven = distance_driven
        self.left_wheel_angle = left_wheel_angle
        self.right_wheel_angle = right_wheel_angle
        self.part_pusher_angle = part_pusher_angle
        self.color_sensor_color = color_sensor_color
        self.distance_sensor_distance = distance_sensor_distance

    def difference(self, previous):
        return SensorReading(
            self.rotation_angle - previous.rotation_angle,
            self.distance_driven - previous.distance_driven,
            self.left_wheel_angle - previous.left_wheel_angle,
            self.right_wheel_angle - previous.right_wheel_angle,
            self.part_pusher_angle - self.part_pusher_angle,
            self.color_sensor_color,  # Don't subtract
            self.distance_sensor_distance - self.distance_sensor_distance
        )


class Calibration:
    def __init__(self):
        self.color_line_white = Colors.WHITE
        self.color_line_black = Colors.BLACK

    def calibrated_color_sensor_color(self, raw):
        return Color(
            util_map(raw.x, self.color_black.x, self.color_white.x, 0, 1, True),
            util_map(raw.y, self.color_black.y, self.color_white.y, 0, 1, True),
            util_map(raw.z, self.color_black.z, self.color_white.z, 0, 1, True)
        )


def get_sensor_reading(environment):
    if environment.simulation:
        from augustyn_tetris_robot.simulation.sensor_reading import get_simulation_sensor_reading
        return get_simulation_sensor_reading(environment)
    else:
        from augustyn_tetris_robot.reality.sensor_reading import get_real_sensor_reading
        return get_real_sensor_reading(get_calibration(environment))


_CACHED_CALIBRATION = None


def get_calibration(environment):
    global _CACHED_CALIBRATION
    if _CACHED_CALIBRATION is None:
        if environment.simulation:
            from augustyn_tetris_robot.reality.calibration import get_real_calibration
            _CACHED_CALIBRATION = get_real_calibration()
            # raise NotImplementedError
            # from augustyn_tetris_robot.simulation.calibration import get_simulation_calibration
            # _CACHED_CALIBRATION = get_simulation_calibration()
        else:
            from augustyn_tetris_robot.reality.calibration import get_real_calibration
            _CACHED_CALIBRATION = get_real_calibration()
    return _CACHED_CALIBRATION
