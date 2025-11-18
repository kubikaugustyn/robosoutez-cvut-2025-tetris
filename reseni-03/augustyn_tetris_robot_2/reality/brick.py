#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import sys
from threading import Thread

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Direction
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from augustyn_tetris_robot_2.reality.calibration import calibrated_color_sensor_reflection


class Brick:
    # SPEED = 1 # Competition speed
    SPEED = 0.5  # Testing speed
    DRIVE_SPEED = 500 * SPEED

    ev3 = EV3Brick()
    left_wheel = Motor(port=Port.B, positive_direction=Direction.COUNTERCLOCKWISE)  # Ideal +-5deg
    right_wheel = Motor(port=Port.D, positive_direction=Direction.COUNTERCLOCKWISE)  # Ideal +-5deg
    # Ideal values are 56 and 184
    wheels = DriveBase(left_wheel, right_wheel, wheel_diameter=54.8, axle_track=175)
    part_pusher = Motor(port=Port.A)  # Ideal +-10deg
    color_sensor = ColorSensor(port=Port.S2)
    distance_sensor = UltrasonicSensor(port=Port.S1)

    # wheels.distance_control.target_tolerances(speed=None, position=1)
    # wheels.heading_control.target_tolerances(speed=None, position=1)
    wheels.distance_control.target_tolerances(speed=None, position=0)
    wheels.heading_control.target_tolerances(speed=None, position=0)
    wheels.settings(
        straight_speed=DRIVE_SPEED,
        straight_acceleration=None,
        turn_rate=None,
        turn_acceleration=None
    )
    print("Settings:", wheels.settings())

    @classmethod
    def measure_reflection(cls):
        return calibrated_color_sensor_reflection(cls.color_sensor.reflection())

    SHUTTING_DOWN = False

    @classmethod
    def may_shutdown(cls):
        if cls.SHUTTING_DOWN:
            raise KeyboardInterrupt("Shutting down.")

    @classmethod
    def shutdown(cls):
        if cls.SHUTTING_DOWN:
            return
        cls.SHUTTING_DOWN = True
        print("Shutting down...")
        for _ in range(20):
            Brick.wheels.stop()
            Brick.left_wheel.brake()
            Brick.right_wheel.brake()
            wait(50)

        print("Goodbye!")
        sys.exit(0)

    @classmethod
    def schedule_shutdown(cls, time_ms=90 * 1000):
        def thread():
            stopwatch = StopWatch()
            stopwatch.resume()
            last_seconds = -1

            while True:
                wait(50)
                if stopwatch.time() > time_ms - 50:
                    cls.shutdown()
                    break
                # print("Stopping in: {:.2f} ms".format(time_ms - stopwatch.time()))

                seconds = (time_ms - stopwatch.time()) / 1000
                if int(seconds) != last_seconds:
                    last_seconds = int(seconds)
                    print("Stopping in: {:.1f} s / runtime: {:.1f} s".format(
                        seconds,
                        stopwatch.time() / 1000
                    ))

        Thread(target=thread).start()
