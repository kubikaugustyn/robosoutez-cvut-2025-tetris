#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import math
from time import time

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.environment.sensors import SensorReading
from augustyn_tetris_robot.fake_np.utils import util_map
from augustyn_tetris_robot.like_ai_brain.goal import GoalStepResult_OK, GoalStepResult_DONE, \
    GoalStepResult_REPLACE_WITH, FollowLineReflectionPGoal, RotateGoal


class Goals:
    _GOALS = {}

    def __init__(self, name, calibration):
        self.name = name
        self.goals = self.get_all_goals(calibration)
        self.current_goal = -1

    @classmethod
    def factory(cls, name):
        def wrapper(calibration):
            return cls._GOALS[name](name, calibration)

        return wrapper

    @classmethod
    def register(cls, name):
        def wrapper(subclass):
            cls._GOALS[name] = subclass
            return subclass

        return wrapper

    @classmethod
    def get_all_goals(cls, calibration):
        raise NotImplementedError("{} doesn't implement get_all_goals()".format(cls.__name__))

    def step(self, environment, sensors, sensor_diff):
        if self.current_goal == -1:
            self.current_goal = 0
            self.goals[0].start(environment, sensors, sensor_diff)

        goal = self.goals[self.current_goal]
        start_time = time()
        if not goal.terminate_condition(environment, sensors, sensor_diff):
            result = goal.step(environment, sensors, sensor_diff)
        else:
            result = GoalStepResult_DONE, None
        end_time = time()
        print("Goal step time: {:.3f} ms".format((end_time - start_time) * 1000))

        if result is None:
            raise ValueError("Goal {} step returned None - not implemented?".format(goal.name))
        if result[0] == GoalStepResult_OK:
            return False
        elif result[0] == GoalStepResult_DONE:
            goal.end(environment, sensors, sensor_diff)
            self.current_goal += 1
            if self.current_goal >= len(self.goals):
                return True
            # Fallthrough to a recursive call
        elif result[0] == GoalStepResult_REPLACE_WITH:
            assert result[1] is not None
            goal.end(environment, sensors, sensor_diff)
            self.goals[self.current_goal:self.current_goal + 1] = result[1]
            # Fallthrough to a recursive call
        else:
            raise ValueError("Unknown goal step result")

        self.goals[self.current_goal].start(environment, sensors, sensor_diff)
        return self.step(environment, sensors, sensor_diff)


@Goals.register("ABYSS")
class AbyssGoals(Goals):
    @classmethod
    def get_all_goals(cls, calibration):
        def is_end_of_line(environment: Environment, sensors: SensorReading,
                           sensor_diff: SensorReading) -> bool:
            diff = sensors.color_sensor_color.distance_sum(calibration.color_line_white)
            if diff > 1.5:
                return False

            if environment.robot.translation.y > 280:
                return False

            return True

        def distance_from_end_of_line(environment: Environment, sensors: SensorReading,
                                      sensor_diff: SensorReading) -> float:
            return util_map(environment.robot.translation.y, 1800, 300, 0, 1, limit=True)

        def is_on_black_line(_, sensors: SensorReading, __) -> bool:
            diff = sensors.color_sensor_color.distance_sum(calibration.color_line_black)
            print("Distance from black:", diff)
            return diff < 1.5

        def is_end_of_line_2(environment: Environment, sensors: SensorReading, _) -> bool:
            diff = sensors.color_sensor_color.distance_sum(calibration.color_line_white)
            if diff > 1.5:
                return False

            if environment.robot.translation.x < 990:
                return False

            return True

        def distance_from_end_of_line_2(environment: Environment, _, __) -> float:
            return util_map(environment.robot.translation.x, 195, 990, 0, 1, limit=True)

        def is_end_of_line_3(environment: Environment, sensors: SensorReading, _) -> bool:
            diff = sensors.color_sensor_color.distance_sum(calibration.color_line_white)
            if diff > 1.5:
                return False

            if environment.robot.translation.x > 195:
                return False

            return True

        def distance_from_end_of_line_3(environment: Environment, _, __) -> float:
            return util_map(environment.robot.translation.x, 990, 195, 0, 1, limit=True)

        return [
            # FollowLineTripleDriveGoal(
            #     calibration.color_line_black,
            #     calibration.color_line_white,
            #     is_end_of_line,
            #     distance_from_end_of_line
            # ),
            # RotateGoal(
            #     math.radians(90),
            #     math.radians(1),
            #     None  # is_on_black_line
            # ),
            # PanicFindLineDriveGoal(
            #     calibration.color_line_black,
            #     False,
            #     None  # is_on_black_line
            # ),
            # FollowLineTripleDriveGoal(
            #     calibration.color_line_black,
            #     calibration.color_line_white,
            #     is_end_of_line_2,
            #     distance_from_end_of_line_2
            # ),
            FollowLineReflectionPGoal(
                is_end_of_line,
                distance_from_end_of_line
            ),
            RotateGoal(
                math.radians(90),
                math.radians(1),
                is_on_black_line
            ),
            FollowLineReflectionPGoal(
                is_end_of_line_2,
                distance_from_end_of_line_2
            ),
            RotateGoal(
                math.radians(180),
                math.radians(1),
                lambda a, b, c: False
            ),
            FollowLineReflectionPGoal(
                is_end_of_line_3,
                distance_from_end_of_line_3
            ),
        ]


# Super, tak tady je 10 tajemných jednoslovných jmen pro operace:
# Obsidian Mirage Eclipse Shadow Veil Abyss Whisper Revenant Lumen Nocturne
GOALS_ABYSS = Goals.factory("ABYSS")


def get_current_goals(calibration) -> Goals:
    return GOALS_ABYSS(calibration)
