cmake_minimum_required(VERSION 3.10)

# Here we have a line comment with weird stuff like #[===]] $#%!#@$!#@%^^%$&%
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

    foreach(ARG ${ARGN})			# Iterate over each argument
        if(${ARG} (MATCHES ("\w+")))
			math(EXPR N "${ARG} * 2")
        else()
        set(a_very_long_invocation_that should_be_just_out the_border_of__80 chars)
        set(a_very_long_invocation_that should_be_just_out the_border_of__80 chars_clearly_so)
        set(a very long invocation that is just below the limit of chars supp)
        						message("${N}") # Print N
this(should
be
wrapped
"adewa")
        endif()
    endforeach()

