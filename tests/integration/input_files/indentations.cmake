cmake_minimum_required(VERSION 3.10)



function(doubleEach)
            foreach(ARG ${ARGN})    # Iterate over each argument
            if(${ARG} MATCHES "\w+" "")
math(EXPR N "${ARG} * 2")
else()
        message("${N}") # Print N
        endif()
    endforeach()
        endfunction()

