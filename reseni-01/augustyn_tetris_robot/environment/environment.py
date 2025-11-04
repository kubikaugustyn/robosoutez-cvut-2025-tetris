#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from augustyn_tetris_robot.environment.objects import EnvironmentObject, Blocks, Block, Robot
from augustyn_tetris_robot.fake_np.polygons import Rectangle, MultiLine, Line
from augustyn_tetris_robot.fake_np.vectors import Colors, Vec2


class Environment:
    objects: list[EnvironmentObject]
    robot: Robot

    def __init__(self, objects: list[EnvironmentObject], robot: Robot) -> None:
        self.objects = objects
        self.robot = robot

    @classmethod
    def normal(cls):
        rows: list[float] = [300 + i * 270 for i in range(5)]
        cols: list[float] = [195 + 289 + i * 193 for i in range(4)]
        blocks: list[list[Block]] = [
            [Blocks.T_NORMAL, Blocks.T_UPSIDE_DOWN, Blocks.T_NORMAL, Blocks.T_UPSIDE_DOWN],
            [Blocks.L_HORIZONTAL, Blocks.L_HORIZONTAL_ROTATED, Blocks.L_HORIZONTAL,
             Blocks.L_HORIZONTAL_ROTATED],
            [Blocks.S, Blocks.S, Blocks.S, Blocks.S],
            [Blocks.I, Blocks.I, Blocks.I, Blocks.I],
            [Blocks.O, Blocks.O, Blocks.O, Blocks.O],
        ]
        blocks_translated: list[EnvironmentObject] = []
        block_outlines_translated: list[EnvironmentObject] = []
        for y, block_row in enumerate(blocks):
            for x, block in enumerate(block_row):
                translation: Vec2 = Vec2(cols[x], rows[y])
                blocks_translated.append(block.translated(translation))
                block_outlines_translated.append(block.outline().translated(translation))

        walls: list[EnvironmentObject] = []
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

        return cls([
            # Walls
            *walls,
            # Black line
            EnvironmentObject(
                MultiLine([
                    # Vertical
                    Line(Vec2(195, 300), Vec2(195, 1680 - 150)),
                    # Horizontal
                    *[
                        Line(Vec2(195, 300 + 270 * i), Vec2(195 + 289 + 193 * 3, 300 + 270 * i))
                        for i in range(5)
                    ],
                ]),
                EnvironmentObject.TYPE_LINE,
                stroke=20,
                stroke_color=Colors.BLACK,
            ),
            # Vertical yellow lines
            EnvironmentObject(
                MultiLine([
                    Line(Vec2(195 + 289 + 193 * i, 300), Vec2(195 + 289 + 193 * i, 300 + 270 * 4))
                    for i in range(4)
                ]),
                EnvironmentObject.TYPE_LINE,
                stroke=20 / 3,
                stroke_color=Colors.YELLOW,
            ),
            # Block outlines
            *block_outlines_translated,
            # Blocks
            *blocks_translated,
        ], Robot(Vec2(1260 / 2, 1680 - 400)))
