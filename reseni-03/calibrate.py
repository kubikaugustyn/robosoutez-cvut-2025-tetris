#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from pybricks.tools import wait

from augustyn_tetris_robot_2.reality.brick import Brick


def main() -> None:
    print("Let's calibrate!")

    # Brick.wheels.straight(1000)
    # Brick.wheels.turn(360 * 5)
    # return

    while True:
        print("Reflection:")
        print("\tRaw:", Brick.color_sensor.reflection())
        print("\tCalibrated:", Brick.measure_reflection())
        print()

        wait(100)


if __name__ == '__main__':
    main()
