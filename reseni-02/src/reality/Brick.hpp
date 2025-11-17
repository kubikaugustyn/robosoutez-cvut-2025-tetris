//
// Created by Jakub Augustýn on 16.11.2025.
// Copyright (c) 2025 Jakub Augustýn. All rights reserved.
//

// #ifndef TETRIS_BRICK_HPP
// #define TETRIS_BRICK_HPP
//
// #endif //TETRIS_BRICK_HPP

#pragma once

#include "../ev3dev.h"

// Jednoduchá C++ verze Brick.py
// Pane Jakube, tohle drží jedinou instanci HW objektů.

class Brick {
public:
    // Motory
    static ev3dev::motor left_wheel;
    static ev3dev::motor right_wheel;
    static ev3dev::motor part_pusher;

    // Senzory
    static ev3dev::color_sensor color_sensor;
    static ev3dev::ultrasonic_sensor distance_sensor;

    // Konstrukce ekvivalentu DriveBase z Pybricks
    // ev3dev nemá DriveBase → uděláme vlastní wrapper
    struct Wheels {
        ev3dev::motor* left;
        ev3dev::motor* right;
        double wheel_diameter;
        double axle_track;

        // Jednoduché API
        void straight(int mm) const;
        void turn(int degrees) const;
        void stop() const;
    };

    static Wheels wheels;

    // Inicializace (jednou na start programu)
    static void init();
};
