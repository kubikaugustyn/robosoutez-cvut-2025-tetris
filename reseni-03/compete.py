#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from pybricks.parameters import Color, Button
from pybricks.tools import wait

from augustyn_tetris_robot_2.goals.follow_line import follow_line_goal, follow_line_backwards_goal
from augustyn_tetris_robot_2.goals.turn_in_place import turn_in_place
from augustyn_tetris_robot_2.reality.brick import Brick


def main() -> None:
    follow_line_goal(1260)
    Brick.wheels.straight(70)
    Brick.wheels.stop()
    turn_in_place(90)
    follow_line_goal(800)
    follow_line_backwards_goal(780, right_side=True)
    Brick.wheels.stop()
    turn_in_place(90)
    follow_line_goal(1260)


if __name__ == '__main__':
    print("Code loaded...")
    while Button.CENTER not in Brick.ev3.buttons.pressed():
        Brick.ev3.light.on(color=Color.ORANGE)
        wait(50)
        Brick.ev3.light.off()
        wait(50)
    print("Let's go!")
    Brick.ev3.light.on(color=Color.GREEN)
    Brick.schedule_shutdown()  # Important for the competition I guess...

    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupt received.")

    Brick.shutdown()
