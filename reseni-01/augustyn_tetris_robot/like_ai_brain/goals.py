#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from augustyn_tetris_robot.environment.environment import Environment
from augustyn_tetris_robot.environment.sensors import SensorReading


class Goals:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def factory(cls, name: str):
        def wrapper():
            return cls(name)

        return wrapper

    def step(self, environment: Environment, sensors: SensorReading,
             sensor_diff: SensorReading) -> None:
        pass


# Super, tak tady je 10 tajemných jednoslovných jmen pro operace:
# Obsidian Mirage Eclipse Shadow Veil Abyss Whisper Revenant Lumen Nocturne
GOALS_ABYSS = Goals.factory("ABYSS")


def get_current_goals() -> Goals:
    return GOALS_ABYSS()
