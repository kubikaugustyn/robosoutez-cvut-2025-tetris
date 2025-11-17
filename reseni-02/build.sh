#!/bin/sh
set -e

clear
cd "/src/build"
cmake .. -DCMAKE_TOOLCHAIN_FILE=../Toolchain-ev3.cmake
make