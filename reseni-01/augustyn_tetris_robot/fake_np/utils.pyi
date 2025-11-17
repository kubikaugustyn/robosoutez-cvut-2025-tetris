#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"

from augustyn_tetris_robot.fake_np.vectors import Scalar


def util_map(x: Scalar, in_min: Scalar, in_max: Scalar, out_min: Scalar,
             out_max: Scalar, limit: bool = False) -> Scalar: ...
