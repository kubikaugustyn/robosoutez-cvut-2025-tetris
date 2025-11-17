#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from typing import Callable, Final, Optional

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.environment.sensors import SensorReading
from augustyn_tetris_robot.fake_np.vectors import Color, Vec3

type Condition = Callable[[Environment, SensorReading, SensorReading], bool]
type Progress = Callable[[Environment, SensorReading, SensorReading], float]

GoalStepResult_OK: Final[int] = ...
GoalStepResult_REPLACE_WITH: Final[int] = ...
GoalStepResult_DONE: Final[int] = ...

type GoalStepResult = tuple[int, list[Goal] | None]


class Goal:
    name: str = ...

    terminate_condition: Condition
    current_progress: Progress

    def __init__(self, terminate_condition: Condition | None = None,
                 current_progress: Progress | None = None) -> None: ...

    def start(self, environment: Environment, sensors: SensorReading,
              sensor_diff: SensorReading) -> None: ...

    def step(self, environment: Environment, sensors: SensorReading,
             sensor_diff: SensorReading) -> GoalStepResult: ...

    def end(self, environment: Environment, sensors: SensorReading,
            sensor_diff: SensorReading) -> None: ...

    @staticmethod
    def slide_sliding_window[T](window: list[T], size: int, value: T) -> None: ...


class FollowLineTripleDriveGoal(Goal):
    color: Color
    ambient_color: Color
    maximum_diff: tuple[float, float, float]
    states: list[tuple[float, float, float]]

    def __init__(self, color: Color, ambient_color: Color,
                 terminate_condition: Condition, current_progress: Progress | None) -> None: ...


class PanicFindLineDriveGoal(Goal):
    color: Color
    direction_left: bool
    start_angle: float

    def __init__(self, color: Color, direction_left: bool,
                 terminate_condition: Condition) -> None: ...


class RotateGoal(Goal):
    angle: float
    tolerance: float
    start_angle: float

    def __init__(self, angle: float, tolerance: float, terminate_condition: Condition) -> None: ...
