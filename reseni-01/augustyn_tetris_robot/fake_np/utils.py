#  -*- coding: utf-8 -*-
__author__ = "Jakub Augustýn <kubik.augustyn@post.cz>"


def util_map(x, in_min, in_max, out_min, out_max, limit=False):
    """
    Re-maps a value from one range to another.

    This function takes a value from one range and maps it proportionally to another range.

    Parameters
    ----------
    x : float
        The input value to be mapped
    in_min : float
        The lower bound of the input range
    in_max : float
        The upper bound of the input range
    out_min : float
        The lower bound of the target range
    out_max : float
        The upper bound of the target range
    limit : bool
        Whether to clamp the output value to the target range or not

    Returns
    -------
    float
        The mapped value in the target range

    Examples
    --------
    >>> util_map(50, 0, 100, 50, 100) # Maps 50 from range 0-100 to range 50-100
    75

    Source: https://docs.arduino.cc/language-reference/en/functions/math/map/
    """
    result = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if limit:
        result = max(min(result, out_max), out_min)
    return result
