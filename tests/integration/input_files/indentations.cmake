cmake_minimum_required(VERSION 3.10)



function(doubleEach)
            foreach(ARG ${ARGN})    # Iterate over each argument
math(EXPR N "${ARG} * 2")
        message("${N}") # Print N
    endforeach()
        endfunction()

