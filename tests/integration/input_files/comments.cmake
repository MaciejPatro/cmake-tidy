


# a very long comment with some text and stuff
# at the beginning of the file - absolutely no need for reading this text - everyone ignores comments either way so please
# do it also in this particular case
if(NOT Value)
# here the comment should be indented
	if(GoogleTest_FOUND AND NOT (TARGET GoogleTest::GoogleTest))
		set(SOME_VALUE ON)

install(TARGETS mylibapp
  RUNTIME
  # TODO: there is some very important information
  # why this silly line of code beneath is really here
  DESTINATION bin
  COMPONENT applications)
    install(FILES "${PYLON_BINARY_DIRS}/PylonUsb_MD_VC120_V5_0_TL.dll" DESTINATION ${CMAKE_INSTALL_BINARY} CONFIGURATIONS Release RelWithDebInfo)


	elseif(CMAKE_GENERATOR STREQUAL "Visual Studio 15 2017"
				OR CMAKE_GENERATOR STREQUAL "Visual Studio 16 2019")
install(# do we handle arguments correctly?
# are you certain?
    EXPORT graphicsmagick-targets
    FILE unofficial-graphicsmagick-targets.cmake # standard line-comment
    NAMESPACE unofficial::graphicsmagick::
    DESTINATION share/unofficial-graphicsmagick
    # we can also check what happens here assuming someone commented out single line
)

	endif()
endif()

