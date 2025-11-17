//
// Created by Jakub Augustýn on 16.11.2025.
// Copyright (c) 2025 Jakub Augustýn. All rights reserved.
//

#include "Brick.hpp"
#include <cmath>
#include <iostream>
#include <thread>

using namespace ev3dev;

// --- Statické instance HW prvků ---

ev3dev::motor Brick::left_wheel(OUTPUT_B);
ev3dev::motor Brick::right_wheel(OUTPUT_D);
ev3dev::motor Brick::part_pusher(OUTPUT_A);

ev3dev::color_sensor Brick::color_sensor(INPUT_2);
ev3dev::ultrasonic_sensor Brick::distance_sensor(INPUT_1);

Brick::Wheels Brick::wheels = {
    &Brick::left_wheel,
    &Brick::right_wheel,
    54.8, // wheel diameter
    180 // axle track
};


// --- Init ---

void Brick::init() {
    // Reset motor positions
    left_wheel.reset();
    right_wheel.reset();
    part_pusher.reset();

    // Reverse direction if needed
    left_wheel.set_polarity(motor::polarity_inversed);
    right_wheel.set_polarity(motor::polarity_inversed);

    if (!color_sensor.connected())
        std::cerr << "Color sensor NOT found!" << std::endl;
    if (!distance_sensor.connected())
        std::cerr << "Ultrasonic sensor NOT found!" << std::endl;
}


// --- Wheels helper function: forward/backward ---

void Brick::Wheels::straight(int mm) const {
    const double mm_per_deg = (M_PI * wheel_diameter) / 360.0;
    int deg = static_cast<int>(mm / mm_per_deg);

    left->set_position_sp(deg).set_speed_sp(200).run_to_rel_pos();
    right->set_position_sp(deg).set_speed_sp(200).run_to_rel_pos();

    while (left->state().count("running") || right->state().count("running"))
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
}


// --- Wheels helper function: turn in place ---

void Brick::Wheels::turn(int degrees) const {
    // Convert robot turn to wheel rotation
    const double turn_circ = M_PI * axle_track;
    double robot_angle_rad = degrees * (M_PI / 180.0);
    double wheel_travel = (robot_angle_rad * axle_track) / 2.0;
    int wheel_degrees = static_cast<int>(wheel_travel * (360.0 / (M_PI * wheel_diameter)));

    left->set_position_sp(wheel_degrees).set_speed_sp(150).run_to_rel_pos();
    right->set_position_sp(-wheel_degrees).set_speed_sp(150).run_to_rel_pos();

    while (left->state().count("running") || right->state().count("running"))
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
}


// --- Wheels stop ---

void Brick::Wheels::stop() const {
    left->stop();
    right->stop();
}
