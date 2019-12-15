cmake_minimum_required(VERSION 3.10)

include(CTest)
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

find_package(GTest REQUIRED)

# Here we have a line comment with weird stuff like #[===]] $#%!#@$!#@%^^%$&%
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

    foreach(ARG ${ARGN})			# Iterate over each argument
        if(${ARG} MATCHES "\w+")
			math(EXPR N "${ARG} * 2")
        else()
        						message("${N}") # Print N
        endif()
    endforeach()

add_subdirectory(       sum_of_non_adjacent )
add_subdirectory(			record_last      			n_logs      )
			add_subdirectory(max_values_subarrays   )
add_subdirectory(string_distance)
	 add_subdirectory(new_dir)
