cmake_minimum_required(VERSION 3.10)




include(CTest)


include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

find_package(GTest REQUIRED)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_subdirectory(string_distance)







