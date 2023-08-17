add_library(_dyn_cudart SHARED cudart_stub.cc)
target_include_directories(_dyn_cudart PUBLIC ${CUDAToolkit_INCLUDE_DIRS})
set_target_properties(_dyn_cudart PROPERTIES INSTALL_RPATH
                                                   "${CUDAToolkit_LIBRARY_DIR}")
if(BUILD_CPP_IF AND NOT BUILD_PY_IF)
  install(
    TARGETS _dyn_cudart
    EXPORT ${CMAKE_PROJECT_NAME}Targets
    DESTINATION lib/)
endif(BUILD_CPP_IF AND NOT BUILD_PY_IF)
if(BUILD_PY_IF)
  install(TARGETS _dyn_cudart DESTINATION mdpu/op/)
endif(BUILD_PY_IF)
