//
// Created by Jakub Augustýn on 16.11.2025.
// Copyright (c) 2025 Jakub Augustýn. All rights reserved.
//

// Přepis původního Python skriptu do C++
// Autor přepis: ChatGPT (pro Pane Jakuba)

#include <iostream>
#include <atomic>
#include <csignal>
#include <thread>
#include <chrono>
#include <exception>

// Předpokládané tvoje C++ hlavičky (přepiš / uprav podle vlastních jmenných prostorů)
// #include "environment/Environment.hpp"
// #include "environment/sensors.hpp"
// #include "fake_np/vectors/Color.hpp"
// #include "like_ai_brain/goals.hpp"
// #include "environment/physics.hpp"
#include <complex>

#include "reality/Brick.hpp"
// #include "reality/render.hpp"
// #include "reality/Timing.hpp"

using namespace std::chrono;

static std::atomic<bool> running{true};

void handle_sigint(int)
{
    running = false;
}

int main()
{
    std::signal(SIGINT, handle_sigint);
    Brick::init();

    try {
        std::cout << "Starting..." << std::endl;

        // vytvořit environment (překlad z Environment.normal(simulation=False))
        // auto environment = Environment::normal(/*simulation=*/false);

        // získat kalibrace / goals
        // auto calibration = get_calibration(environment);
        // auto goals = get_current_goals(calibration);

        // předchozí čtení senzorů
        // auto prev_sensors = get_sensor_reading(environment);

        // Timing timing;

        std::cout << "Ready. Going now..." << std::endl;

        while (running) {
            // timing.loop_start();

            // Read sensors
            // timing.read_sensors();
            // auto sensors = get_sensor_reading(environment);

            // sensor diff (předpokládáme, že sensors má metodu difference)
            // auto sensor_diff = sensors.difference(prev_sensors);
            // prev_sensors = sensors;

            // Update inner state (physics)
            // timing.physics();
            // physics::step(environment, sensors, sensor_diff);

            // Decide what to do next (goals)
            // timing.goals();
            // bool done = goals->step(environment, sensors, sensor_diff);
            // if (done) {
                // std::cout << "All goals done, quitting..." << std::endl;
                // break;
            // }

            // Render for user
            // timing.render();
            // render(environment, *goals, timing);

            // timing.loop_end();

            Brick::wheels.straight(1000);
            break;

            std::this_thread::sleep_for(milliseconds(100));
        }

        // stop motors / parts
        Brick::wheels.stop();
        Brick::part_pusher.stop();

        std::cout << "Done." << std::endl;
    }
    catch (const std::exception &e) {
        std::cerr << "Unhandled exception: " << e.what() << std::endl;
        // zkusme bezpečně zastavit hardware při chybě
        try {
            Brick::wheels.stop();
            Brick::part_pusher.stop();
        } catch (...) { /* ignore */ }
        return 1;
    }

    return 0;
}

/*
#include <iostream>
#include <ostream>
#include <thread>

#include "ev3dev.h"

using namespace std;
using namespace ev3dev;
large_motor motor1, motor2;

int main() {
    std::cout << "Hello World! Kuba here!" << std::endl;

    motor1 = large_motor(OUTPUT_B);
    motor1.set_speed_sp(500);
    motor1.set_time_sp(5000).run_timed();

    motor2 = large_motor(OUTPUT_D);
    motor2.set_speed_sp(500);
    motor2.set_time_sp(5000).run_timed();

    while (motor1.state().count("running") || motor2.state().count("running"))
        this_thread::sleep_for(chrono::milliseconds(10));

    motor1.set_stop_action("brake");
    motor2.set_stop_action("brake");
    motor1.stop();
    motor2.stop();

    return 0;
}
*/
