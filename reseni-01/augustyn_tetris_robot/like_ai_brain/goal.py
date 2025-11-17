#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import math

from augustyn_tetris_robot.reality.brick import Brick

GoalStepResult_OK = 1
GoalStepResult_REPLACE_WITH = 2
GoalStepResult_DONE = 3


class Goal:
    name = "Unnamed goal"

    def __init__(self, terminate_condition=None, current_progress=None):
        if terminate_condition is None:
            self.terminate_condition = lambda a, b, c: False
        else:
            self.terminate_condition = terminate_condition

        if current_progress is None:
            self.current_progress = lambda a, b, c: 0.0
        else:
            self.current_progress = current_progress

    def start(self, environment, sensors, sensor_diff):
        pass

    def step(self, environment, sensors, sensor_diff):
        raise NotImplementedError("{} doesn't implement step()".format(type(self).__name__))

    def end(self, environment, sensors, sensor_diff):
        pass

    @staticmethod
    def slide_sliding_window(window, size, value):
        if len(window) < size:
            window.append(value)
            return

        for i in range(len(window) - 1):
            window[i] = window[i + 1]
        window[-1] = value


class FollowLineTripleDriveGoal(Goal):
    DIFF_MIDDLE_THRESHOLD = 0.1
    DIFF_THRESHOLD = 0.4
    SLIDING_WINDOW = 5
    # Gain inspired by https://pybricks.com/ev3-micropython/examples/robot_educator_line.html
    # Set the gain of the proportional line controller. This means that for every
    # percentage point of light deviating from the threshold, we set the turn
    # rate of the drive base to 1.2 degrees per second.
    # For example, if the light value deviates from the threshold by 10, the robot
    # steers at 10*1.2 = 12 degrees per second.
    PROPORTIONAL_GAIN = 30

    name = "Follow a line and drive goal using a 'tripled' sensor"

    def __init__(self, color, ambient_color, terminate_condition, current_progress):
        super().__init__(terminate_condition, current_progress)
        self.color = color
        self.ambient_color = ambient_color
        self.maximum_diff = color.distance_tuple(ambient_color)
        self.states = []

    @staticmethod
    def k(progress):
        if progress <= 0.8:
            return 1.0
        # lineární pokles z 1.0 na 0.25 mezi 0.8–1.0
        t = (progress - 0.8) / 0.2  # t jde 0 → 1
        return 1.0 - 0.75 * t

    def step(self, environment, sensors, sensor_diff):
        # This uses a trick with the color sensor abusing the fact the color sensor has the three
        # colors in the LED slightly offset, so we can pretend we have three color sensors
        # The order on our robot is left: blue, middle: red, right: green.
        rel_diff = sensors.color_sensor_color.rel_distance_tuple(self.color, self.maximum_diff)
        rel_diff_middle, rel_diff_right, rel_diff_left = rel_diff

        print("Diff left: {}%, diff middle: {}%, diff right: {}%".format(
            int(rel_diff_left * 100),
            int(rel_diff_middle * 100),
            int(rel_diff_right * 100)
        ))

        k = self.k(self.current_progress(environment, sensors, sensor_diff))
        drive_speed = 250 * k

        if rel_diff_middle < self.DIFF_MIDDLE_THRESHOLD:
            print("Great, continue forward")
            # Brick.wheels.drive(drive_speed, 0)
            self.states.clear()
        else:
            trend_left, trend_right = 0, 0
            states = self.states
            if len(states) >= 2:
                trend_left = states[0][0] - states[-1][0]
                trend_right = states[0][2] - states[-1][2]
            print("Trend - left: {:.3f}, right: {:.3f}".format(trend_left, trend_right))

            panic = False
            if rel_diff_left < rel_diff_right:
                if trend_right >= -self.DIFF_THRESHOLD:
                    print("Slightly left")
                    # Brick.wheels.drive(drive_speed, -self.PROPORTIONAL_GAIN * rel_diff_right * k)
                else:
                    panic = True
            else:
                if trend_left >= -self.DIFF_THRESHOLD:
                    print("Slightly right")
                    # Brick.wheels.drive(drive_speed, self.PROPORTIONAL_GAIN * rel_diff_left * k)
                else:
                    panic = True

            # if panic:
            #     return GoalStepResult_REPLACE_WITH, [
            #         PanicFindLineDriveGoal(
            #             self.color,
            #             trend_left > trend_right,
            #             self.terminate_condition,
            #         ),
            #         self
            #     ]

        self.slide_sliding_window(self.states, self.SLIDING_WINDOW,
                                  (rel_diff_left, rel_diff_middle, rel_diff_right))
        return GoalStepResult_OK, None


class FollowLineReflectionPGoal(Goal):
    THRESHOLD = .5  # ručně zadaná středová hodnota
    PROPORTIONAL_GAIN = 60  # jako pybricks tutorial
    DRIVE_SPEED = 250  # mm/s

    name = "Follow line using luminance-based P-control"

    def __init__(self, terminate_condition, current_progress):
        super().__init__(terminate_condition, current_progress)

    @staticmethod
    def luminance(rgb):
        r, g, b = rgb
        # Rec.709 luminance – stabilní, odolná vůči šumu
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    @staticmethod
    def k(progress):
        if progress <= 0.8:
            return 1.0
        # lineární pokles z 1.0 na 0.25 mezi 0.8–1.0
        t = (progress - 0.8) / 0.2  # t jde 0 → 1
        return 1.0 - 0.75 * t

    def step(self, environment, sensors, sensor_diff):
        k = self.k(self.current_progress(environment, sensors, sensor_diff))

        rgb = sensors.color_sensor_color
        reflection = self.luminance(rgb)
        deviation = reflection - self.THRESHOLD
        # 4) P-regulace — čistý PyBricks styl
        turn = deviation * self.PROPORTIONAL_GAIN
        Brick.wheels.drive(self.DRIVE_SPEED * k, turn * k)

        return GoalStepResult_OK, None


class PanicFindLineDriveGoal(Goal):
    DIFF_THRESHOLD = 0.1

    name = "Panic line-finding goal"

    def __init__(self, color, direction_left, terminate_condition):
        super().__init__(terminate_condition)
        self.color = color
        self.direction_left = direction_left
        self.start_angle = float('nan')

    def start(self, environment, sensors, sensor_diff):
        self.start_angle = Brick.wheels.angle()
        print("Start at angle:", self.start_angle)

    def step(self, environment, sensors, sensor_diff):
        angle = Brick.wheels.angle()
        diff_angle = angle - self.start_angle
        print("Current diff angle:", diff_angle)
        if self.direction_left:
            Brick.wheels.drive(0, -40)
            if diff_angle <= 45:
                self.direction_left = False
        else:
            Brick.wheels.drive(0, 40)
            if diff_angle <= -45:
                self.direction_left = True

        diff = sensors.color_sensor_color.distance_sum(self.color)
        if diff > self.DIFF_THRESHOLD * 3:
            print("Line not found, turning left:", self.direction_left)
            return GoalStepResult_OK, None
        else:
            print("Line found")
            return GoalStepResult_DONE, None


class RotateGoal(Goal):
    name = "Rotate goal"

    def __init__(self, angle, tolerance, terminate_condition):
        super().__init__(terminate_condition)
        self.angle = angle
        self.tolerance = tolerance
        self.start_angle = float('nan')

    def start(self, environment, sensors, sensor_diff):
        self.start_angle = math.radians(Brick.wheels.angle())

    def step(self, environment, sensors, sensor_diff):
        angle = math.radians(Brick.wheels.angle()) - self.start_angle
        missing_deg = math.degrees(self.angle - angle)
        print("Turn by {:.1f}deg".format(missing_deg))
        if -self.tolerance < self.angle - angle < self.tolerance:
            return GoalStepResult_DONE, None
        else:
            Brick.wheels.turn(missing_deg)
            return GoalStepResult_OK, None
