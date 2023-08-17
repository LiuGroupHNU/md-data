cmake_minimum_required(VERSION 3.9)
project(mdpu_api_c_test)

file(GLOB TEST_SRC test_*.cc)

set_target_properties(
  ${LIB_MDPU_C} PROPERTIES INSTALL_RPATH "$ORIGIN;${TensorFlow_LIBRARY_PATH}")

add_executable(runUnitTests_c ${TEST_SRC})
target_link_libraries(runUnitTests_c PRIVATE GTest::gtest_main ${LIB_MDPU_C}
                                             rt coverage_config)
target_link_libraries(runUnitTests_c PRIVATE ${LIB_MDPU} ${LIB_MDPU_CC})
target_precompile_headers(runUnitTests_c PRIVATE test_utils.h [["mdpu.hpp"]])
add_test(runUnitTests_c runUnitTests_c)
set_target_properties(runUnitTests_c PROPERTIES INSTALL_RPATH "$ORIGIN/../lib")
install(TARGETS runUnitTests_c DESTINATION bin/)
