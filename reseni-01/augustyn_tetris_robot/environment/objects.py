#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from augustyn_tetris_robot.fake_np.polygons import AbstractPolygon, Rectangle, MultiPolygon, \
    MultiLine, Line
from augustyn_tetris_robot.fake_np.vectors import Color, Colors, Vec2, Scalar


class EnvironmentObject:
    TYPE_WALL = 1
    TYPE_BLOCK = 2
    TYPE_LINE = 3
    TYPE_ROBOT = 4

    geom: AbstractPolygon
    type_: int
    stroke: Scalar | None
    stroke_color: Color | None
    fill: Color | None

    def __init__(self, geom: AbstractPolygon, type_: int, *, stroke: Scalar | None = None,
                 stroke_color: Color | None = None, fill: Color | None = None) -> None:
        self.geom = geom
        self.type_ = type_
        self.stroke = stroke
        assert stroke_color is not None if stroke is not None else stroke_color is None
        self.stroke_color = stroke_color
        self.fill = fill

    def translated(self, translation: Vec2) -> "EnvironmentObject":
        return EnvironmentObject(self.geom.translated(translation), self.type_, stroke=self.stroke,
                                 stroke_color=self.stroke_color, fill=self.fill)


class Block(EnvironmentObject):
    def __init__(self, geom_str: str, origin: Vec2, color: Color) -> None:
        super().__init__(self._generate_geom(geom_str).translated(origin * 40),
                         EnvironmentObject.TYPE_BLOCK, fill=color)

    @staticmethod
    def _generate_geom(geom_str: str) -> AbstractPolygon:
        rectangles: list[Rectangle] = []
        for y, line in enumerate(geom_str.split("\n")):
            for x, char in enumerate(line):
                if char == "#":
                    rectangles.append(Rectangle.from_top_left_width_height(y * 40, x * 40, 40, 40))
                elif char == " ":
                    pass
                else:
                    raise ValueError(f"Unknown character in geometry: '{char}'")
        return MultiPolygon(rectangles)

    def outline(self) -> EnvironmentObject:
        return EnvironmentObject(self.geom, EnvironmentObject.TYPE_LINE, stroke=20 / 6,
                                 stroke_color=self.fill)


class Blocks:
    T_NORMAL = Block("###\n # ", Vec2(-1, -1.5), Colors.YELLOW)
    T_UPSIDE_DOWN = Block(" # \n###", Vec2(-1, -1.5), Colors.YELLOW)
    L_HORIZONTAL = Block("###\n#  ", Vec2(-1, -1.5), Colors.RED)
    L_HORIZONTAL_ROTATED = Block("  #\n###", Vec2(-1, -1.5), Colors.RED)
    S = Block("## \n ##", Vec2(-1, -0.5), Colors.BLACK)
    I = Block("####", Vec2(-2, -0.5), Colors.GREEN)
    O = Block("##\n##", Vec2(-1, -1), Colors.BLUE)


class Robot:
    rotation: float  # in radians # FIXME Use the rotation
    translation: Vec2
    origin: Vec2
    base_geom: AbstractPolygon

    # Moving claw
    part_pusher_rotation: float
    # Pusher, axle1, axle2
    part_pusher_starting: tuple[AbstractPolygon, AbstractPolygon, AbstractPolygon]
    part_pusher_joints: tuple[None, Vec2, Vec2]
    # Color sensor
    color_sensor: Vec2  # Origin
    # Distance sensor
    distance_sensor: tuple[Vec2, Vec2]  # Origin, direction normalized vector
    # Wheels
    wheels: tuple[Vec2, Vec2]  # Translations from the origin
    wheel_diameter: Scalar = 56

    def __init__(self, origin: Vec2) -> None:
        self.translation = origin
        self.rotation = 0
        self.part_pusher_rotation = 0
        self._generate_geom()

    def _generate_geom(self) -> None:
        self.origin = Vec2(0, 0)  # In the middle of the wheels

        static_claw_origin: Vec2 = Vec2(- 200 / 2, -92)  # Bottom left corner
        part_pusher_origin: Vec2 = static_claw_origin + Vec2(0, -112)  # Top left corner
        self.part_pusher_starting = tuple(map(lambda x: x.translated(part_pusher_origin), (
            Line(Vec2(150, 112), Vec2(150, 0)),
            Line(Vec2(0, 0), Vec2(150, 0)),
            Line(Vec2(0, 48), Vec2(150, 48))
        )))
        self.part_pusher_joints = (None, part_pusher_origin, part_pusher_origin + Vec2(0, 48))

        self.color_sensor = Vec2(0, -72)

        self.distance_sensor = (Vec2(0, -230), Vec2(0, -1))

        self.wheels = (Vec2(-184 / 2, 0), Vec2(184 / 2, 0))

        self.base_geom = MultiPolygon([
            # Wheels and stuff
            Rectangle.from_top_left_width_height(-55 / 2, -215 / 2, 215, 55),
            MultiLine([
                Line(Vec2(-48, -55 / 2), static_claw_origin),
                Line(Vec2(48, -55 / 2), static_claw_origin + Vec2(200, 0)),
            ]),
            # The static claw part
            MultiLine([
                Line(Vec2(0, -112), Vec2(0, 0)),
                Line(Vec2(0, 0), Vec2(200, 0)),
                Line(Vec2(200, 0), Vec2(200, -140)),
            ]).translated(static_claw_origin),
            # The moving claw part is added in as_object()
        ])

    def as_object(self) -> EnvironmentObject:
        return EnvironmentObject(
            self.geom,
            EnvironmentObject.TYPE_ROBOT,
            stroke=2, stroke_color=Colors.CYAN
        )

    @property
    def geom(self) -> AbstractPolygon:
        geom: AbstractPolygon = MultiPolygon([
            self.base_geom,
            *self.part_pusher
        ])
        if self.rotation != 0:
            geom = geom.copy_rotated(self.origin, self.rotation)
        return geom.translated(self.translation)

    @property
    def part_pusher(self) -> tuple[AbstractPolygon, AbstractPolygon, AbstractPolygon]:
        axle1 = self.part_pusher_starting[1].copy_rotated(self.part_pusher_joints[1],
                                                          self.part_pusher_rotation)
        axle2 = self.part_pusher_starting[2].copy_rotated(self.part_pusher_joints[2],
                                                          self.part_pusher_rotation)
        return (
            # This one doesn't rotate
            self.part_pusher_starting[0].translated(
                axle1.vertices()[1] - self.part_pusher_starting[1].vertices()[1]
            ),
            axle1,
            axle2,
        )
