cmake_minimum_required(VERSION 3.7.2)
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

# cesta k tvému Linaro 5.5 toolchainu
set(CMAKE_C_COMPILER   /usr/bin/arm-linux-gnueabi-gcc)
set(CMAKE_CXX_COMPILER /usr/bin/arm-linux-gnueabi-g++)
#set(CMAKE_FIND_ROOT_PATH /home/kubik/gcc-linaro-5.5.0/arm-linux-gnueabi)