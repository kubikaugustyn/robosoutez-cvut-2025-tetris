#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

import math

import cv2

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.simulation.render import render
import augustyn_tetris_robot.environment.physics as physics

# SCALE:float=0.75
SCALE: float = 0.45


def main() -> None:
    environment: Environment = Environment.normal()

    step: int = 0
    while True:
        environment.robot.part_pusher_rotation = -math.pi / 4 * math.fabs(math.sin(step / 100))
        environment.robot.translation.y -= 5
        physics.step(environment)
        step += 1

        img = render(environment)

        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img_small = cv2.resize(img_bgr, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_AREA)
        cv2.imshow("Environment", img_small)
        key: int = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord("s"):
            cv2.imwrite("save.png", img_bgr)
            print("Image saved to save.png")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
