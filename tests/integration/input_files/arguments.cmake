cmake_minimum_required(VERSION 3.10)

include(CTest)
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

find_package(GTest REQUIRED)

# Here we have a line comment with weird stuff like #[===]] $#%!#@$!#@%^^%$&%
set([==[ currently a weird bracket argument introduced
some 2839697%%*^$& text ]===] fake close and stuff]==] some
    other
    [===[www]===]
    [======[this
    should
    be
    indented differently
]======]
    "quoted argument with \" escaped quote")

set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_subdirectory(sum_of_non_adjacent)
add_subdirectory(record_last_n_logs)
add_subdirectory(max_values_subarrays)
add_subdirectory(string_distance)
