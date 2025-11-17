#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from time import time

from pybricks.parameters import Color as PybricksColor
from pybricks.media.ev3dev import Font

from augustyn_tetris_robot.reality.brick import Brick

tiny_font = Font(size=6)


class Timing:
    def __init__(self):
        self.start_loop = 0
        self.start_read_sensors = 0
        self.start_physics = 0
        self.start_goals = 0
        self.start_render = 0
        self.end_loop = 0

        self.time_loop = 0
        self.time_read_sensors = 0
        self.time_physics = 0
        self.time_goals = 0
        self.time_render = 0

    def loop_start(self):
        self.start_loop = time()

    def read_sensors(self):
        self.start_read_sensors = time()

    def physics(self):
        self.start_physics = time()
        self.time_read_sensors = self.start_physics - self.start_read_sensors

    def goals(self):
        self.start_goals = time()
        self.time_physics = self.start_goals - self.start_physics

    def render(self):
        self.start_render = time()
        self.time_goals = self.start_render - self.start_goals

    def loop_end(self):
        self.end_loop = time()
        self.time_render = self.end_loop - self.start_render
        self.time_loop = self.end_loop - self.start_loop
        print(
            "Loop took {:.2f} ms - sensors {:.2f} ms, physics {:.2f} ms, "
            "goals {:.2f} ms, render {:.2f} ms".format(
                self.time_loop * 1000,
                self.time_read_sensors * 1000,
                self.time_physics * 1000,
                self.time_goals * 1000,
                self.time_render * 1000,
            )
        )
        print()  # Newline

    def compact_time(self):
        return ("Loop {:.2f} - Sensors {:.2f}\nPhysics {:.2f} Goals {:.2f} Render {:.2f}".format(
            self.time_loop * 1000,
            self.time_read_sensors * 1000,
            self.time_physics * 1000,
            self.time_goals * 1000,
            self.time_render * 1000,
        ))


def render(environment, goal, timing):
    # for obj in environment.objects:
    #     _render_object(img, obj.translated(translation))

    # _render_object(img, environment.robot.as_object().translated(translation))
    return

    sc = Brick.ev3.screen
    white, black = PybricksColor.WHITE, PybricksColor.BLACK
    sc.clear()

    # Timing
    sc.draw_line(0, 20, sc.width, 20, width=1, color=black)
    sc.set_font(tiny_font)
    line1, line2 = timing.compact_time().split("\n", 1)
    sc.draw_text(0, 0, line1, text_color=black, background_color=white)
    sc.draw_text(0, 10, line2, text_color=black, background_color=white)
