################################################
# BLABLA
################################################

cmake_minimum_required(VERSION 3.13 FATAL_ERROR)
project(A_PROJECT)

find_package(Library REQUIRED)

add_library(${PROJECT_NAME})
add_library(${PROJECT_NAME}::${PROJECT_NAME} ALIAS ${PROJECT_NAME})

set_target_properties(${PROJECT_NAME}
	PROPERTIES
		FOLDER Components
)

target_sources(${PROJECT_NAME}
	PRIVATE
		${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
		${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
		${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
		${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
		${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
		${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
		${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
		${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
)

if(${CMAKE_SYSTEM_NAME} STREQUAL Windows OR ${CMAKE_SYSTEM_NAME} STREQUAL Linux)
	target_sources(${PROJECT_NAME}
		PRIVATE
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
	)
endif()

set_property(
	SOURCE
		${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
	PROPERTY COMPILE_FLAGS
		$<$<CXX_COMPILER_ID:MSVC>:/Y-> # ignore precompiled headers
)

target_link_libraries(${PROJECT_NAME}
	PUBLIC
		boost::boost
	PRIVATE
		$<$<PLATFORM_ID:Linux>:pthread>
)

target_include_directories(${PROJECT_NAME}
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/HALLO>
	PRIVATE
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/MALLOW>
)

include(CMakePackage OPTIONAL)
if(COMMAND target_set)
	target_set(${PROJECT_NAME}
		GROUP
			File.cpp
		DIRECTORY
			${CMAKE_CURRENT_SOURCE_DIR}/Source/File.cpp
	)
endif()

################################################
# BLABLA
################################################
add_custom_command(
TARGET
        ${_TARGET}
        POST_BUILD
        )