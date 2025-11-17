cmake_minimum_required(VERSION 3.7.2)
project(tetris)

set(CMAKE_CXX_STANDARD 11)

add_executable(tetris src/main.cpp src/ev3dev.cpp
        src/reality/Brick.hpp
        src/reality/Brick.cpp)
