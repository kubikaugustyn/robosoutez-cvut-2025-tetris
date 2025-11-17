#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import time

from pybricks.media.ev3dev import Font
from pybricks.tools import wait

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.environment.sensors import get_sensor_reading, get_calibration
from augustyn_tetris_robot.fake_np.vectors import Color
from augustyn_tetris_robot.like_ai_brain.goals import get_current_goals
import augustyn_tetris_robot.environment.physics as physics
from augustyn_tetris_robot.reality.brick import Brick
from augustyn_tetris_robot.reality.render import render, Timing


def main():
    print("Starting...")
    environment = Environment.normal(simulation=False)
    goals = get_current_goals(get_calibration(environment))
    prev_sensors = get_sensor_reading(environment)
    timing = Timing()
    print("Ready. Going now...")

    # Brick.wheels.straight(1000)
    # Brick.wheels.straight(1600 - 350)
    # Brick.wheels.turn(360 * 5)
    # for _ in range(3):
    #     Brick.wheels.turn(15)
    #     print(Brick.wheels.angle())
    #     Brick.wheels.turn(-15)
    #     print(Brick.wheels.angle())
    # return

    while True:
        timing.loop_start()

        # Read sensors
        timing.read_sensors()
        sensors = get_sensor_reading(environment)
        sensor_diff = sensors.difference(prev_sensors)
        prev_sensors = sensors

        # Update the inner state
        timing.physics()
        physics.step(environment, sensors, sensor_diff)

        # Decide what to do next
        timing.goals()
        done = goals.step(environment, sensors, sensor_diff)
        if done:
            print("All goals done, quitting...")
            break

        # Show it to the user
        timing.render()
        render(environment, goals, timing)

        # Tmp
        # sc = Brick.ev3.screen
        # sc.set_font(Font(size=20))
        # sc.draw_text(50, 50, str(sensors.color_sensor_color.x))
        # sc.draw_text(50, 70, str(sensors.color_sensor_color.y))
        # sc.draw_text(50, 90, str(sensors.color_sensor_color.z))
        # print(sensors.color_sensor_color.ansi_bg_colorize("   Color   "), end=" ")
        # r, g, b = sensors.color_sensor_color
        # print(Color(r, r, r).ansi_bg_colorize(" {} ".format(str(int(r * 255)).center(3))), end=" ")
        # print(Color(g, g, g).ansi_bg_colorize(" {} ".format(str(int(g * 255)).center(3))), end=" ")
        # print(Color(b, b, b).ansi_bg_colorize(" {} ".format(str(int(b * 255)).center(3))))

        timing.loop_end()
        # sleep(0.1) Damn it this took me 1 day to realize
        # wait(1)

    Brick.wheels.stop()
    Brick.left_wheel.brake()
    Brick.right_wheel.brake()
    Brick.part_pusher.stop()
    print("Done.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user, quitting...")
