#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from augustyn_tetris_robot.environment.objects import EnvironmentObject, Blocks, Block, Robot
from augustyn_tetris_robot.fake_np.polygons import Rectangle, MultiLine, Line
from augustyn_tetris_robot.fake_np.vectors import Colors, Vec2


class Environment:
    def __init__(self, simulation, objects, robot):
        self.simulation = simulation
        self.objects = objects
        self.robot = robot

    @classmethod
    def normal(cls, *, simulation):
        rows = [300 + i * 270 for i in range(5)]
        cols = [195 + 289 + i * 193 for i in range(4)]
        blocks = [
            [Blocks.T_NORMAL, Blocks.T_UPSIDE_DOWN, Blocks.T_NORMAL, Blocks.T_UPSIDE_DOWN],
            [Blocks.L_HORIZONTAL, Blocks.L_HORIZONTAL_ROTATED, Blocks.L_HORIZONTAL,
             Blocks.L_HORIZONTAL_ROTATED],
            [Blocks.S, Blocks.S, Blocks.S, Blocks.S],
            [Blocks.I, Blocks.I, Blocks.I, Blocks.I],
            [Blocks.O, Blocks.O, Blocks.O, Blocks.O],
        ]
        blocks_translated = []
        block_outlines_translated = []
        for y, block_row in enumerate(blocks):
            for x, block in enumerate(block_row):
                translation = Vec2(cols[x], rows[y])
                blocks_translated.append(block.translated(translation))
                block_outlines_translated.append(block.outline().translated(translation))

        walls = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                walls.append(EnvironmentObject(
                    Rectangle.from_top_left_width_height(y * 1680, x * 1260, 1260, 1680),
                    EnvironmentObject.TYPE_WALL,
                    stroke=10,
                    stroke_color=Colors.BLACK,
                    fill=Colors.WHITE,
                ))

        return cls(
            simulation,
            (
                # Walls
                    walls +
                    # Vertical yellow lines
                    [EnvironmentObject(
                        MultiLine([
                            Line(Vec2(195 + 289 + 193 * i, 300),
                                 Vec2(195 + 289 + 193 * i, 300 + 270 * 4))
                            for i in range(4)
                        ]),
                        EnvironmentObject.TYPE_LINE,
                        stroke=20 / 3,
                        stroke_color=Colors.YELLOW,
                    )] +
                    # Target yellow area
                    [EnvironmentObject(
                        Rectangle
                        .from_top_left_width_height(1680 - 400, 0, 400, 400)
                        .translated(Vec2(10, -10)),
                        EnvironmentObject.TYPE_LINE,
                        stroke=20 / 3,
                        stroke_color=Colors.YELLOW,
                    )] +
                    # Block outlines
                    block_outlines_translated +
                    # Black line
                    [EnvironmentObject(
                        MultiLine(
                            # Vertical
                            [Line(Vec2(195, 300), Vec2(195, 1680 - 150))] +
                            # Horizontal
                            [
                                Line(Vec2(195, 300 + 270 * i),
                                     Vec2(195 + 289 + 193 * 3, 300 + 270 * i))
                                for i in range(5)
                            ]
                        ),
                        EnvironmentObject.TYPE_LINE,
                        stroke=20,
                        stroke_color=Colors.BLACK,
                    )] +
                    # Blocks
                    blocks_translated
            ),
            # Robot(Vec2(1260 / 2, 1680 - 400))
            # Robot(Vec2(1260 / 2, 1680 / 2))
            Robot(Vec2(195, 1680 - 80))
            # Robot(Vec2(195, 350))
            # Robot(Vec2(990, 300))
        )
