# new in 3.16: GET_RUNTIME_DEPENDENCIES, target_precompile_headers
cmake_minimum_required(VERSION 3.16)
project(MDPU)

option(BUILD_TESTING "Build test and enable converage" OFF)
set(MDPU_C_ROOT
    ""
    CACHE PATH "Path to imported mdpu-kit C library")

if(BUILD_TESTING)
  enable_testing()
  add_subdirectory(${CMAKE_SOURCE_DIR}/cmake/coverage_config coverage_config)
endif()

# build cpp or python interfaces
if(NOT DEFINED BUILD_CPP_IF)
  set(BUILD_CPP_IF TRUE)
endif(NOT DEFINED BUILD_CPP_IF)
if(NOT DEFINED BUILD_PY_IF)
  set(BUILD_PY_IF FALSE)
endif(NOT DEFINED BUILD_PY_IF)
if((NOT BUILD_PY_IF) AND (NOT BUILD_CPP_IF))
  # nothing to do
  message(FATAL_ERROR "Nothing to do.")
endif()

if(BUILD_CPP_IF AND BUILD_TESTING)
  if(NOT INSTALL_TENSORFLOW)
    # some errors in conda packages...
    find_package(GTest)
  endif()
  if(NOT GTEST_LIBRARIES)
    configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/googletest.cmake.in
                   googletest-download/CMakeLists.txt @ONLY)
    execute_process(
      COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" .
      RESULT_VARIABLE result
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download)
    if(result)
      message(FATAL_ERROR "CMake step for googletest failed: ${result}")
    endif()
    execute_process(
      COMMAND ${CMAKE_COMMAND} --build .
      RESULT_VARIABLE result
      WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download)
    if(result)
      message(FATAL_ERROR "Build step for googletest failed: ${result}")
    endif()
    set(gtest_force_shared_crt
        ON
        CACHE BOOL "" FORCE)
    add_subdirectory(
      ${CMAKE_CURRENT_BINARY_DIR}/googletest-src
      ${CMAKE_CURRENT_BINARY_DIR}/googletest-build EXCLUDE_FROM_ALL)
  endif()
endif()

find_package(Git)
if(GIT_FOUND)
  execute_process(
    COMMAND git describe --tags --dirty
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    OUTPUT_VARIABLE GIT_SUMM
    OUTPUT_STRIP_TRAILING_WHITESPACE)
  execute_process(
    COMMAND git log -1 --format=%h
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    OUTPUT_VARIABLE GIT_HASH
    OUTPUT_STRIP_TRAILING_WHITESPACE)
  execute_process(
    COMMAND git rev-parse --abbrev-ref HEAD
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    OUTPUT_VARIABLE GIT_BRANCH
    OUTPUT_STRIP_TRAILING_WHITESPACE)
  execute_process(
    COMMAND git show -s --format=%ci ${GIT_HASH}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    OUTPUT_VARIABLE GIT_DATE
    OUTPUT_STRIP_TRAILING_WHITESPACE)
endif(GIT_FOUND)

# global defines
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/)

# model version
file(READ ${PROJECT_SOURCE_DIR}/config/MODEL_VER MODEL_VERSION)
string(REPLACE "\n" " " MODEL_VERSION ${MODEL_VERSION})
message(STATUS "Supported model version: ${MODEL_VERSION}")

# Devices that have both ROCM and CUDA are not currently supported
if(USE_ROCM_TOOLKIT AND USE_CUDA_TOOLKIT)
  message(
    FATAL_ERROR
      "Devices that have both ROCM and CUDA are not currently supported")
endif()
set(DP_VARIANT "cpu")

# define USE_CUDA_TOOLKIT
if(USE_CUDA_TOOLKIT)
  cmake_minimum_required(VERSION 3.23)
  find_package(CUDAToolkit REQUIRED)
  if(NOT DEFINED CMAKE_CUDA_COMPILER)
    set(CMAKE_CUDA_COMPILER ${CUDAToolkit_NVCC_EXECUTABLE})
  endif()
  if(NOT DEFINED CMAKE_CUDA_HOST_COMPILER)
    set(CMAKE_CUDA_HOST_COMPILER ${CMAKE_CXX_COMPILER})
  endif()
  add_definitions("-DGOOGLE_CUDA")
  message(STATUS "Found CUDA in ${CUDAToolkit_BIN_DIR}, build nv GPU support")
  set(DP_VARIANT "cuda")
else()
  message(STATUS "Will not build nv GPU support")
endif(USE_CUDA_TOOLKIT)

# define USE_ROCM_TOOLKIT
if(USE_ROCM_TOOLKIT)
  cmake_minimum_required(VERSION 3.21)
  find_package(ROCM REQUIRED)
  add_definitions("-DTENSORFLOW_USE_ROCM")
  add_compile_definitions(__HIP_PLATFORM_HCC__)
  message(STATUS "Found ROCM in ${ROCM_ROOT}, build AMD GPU support")
  set(DP_VARIANT "rocm")
else()
  message(STATUS "Will not build AMD GPU support")
endif(USE_ROCM_TOOLKIT)

set(MDPU_SOURCE_DIR ${PROJECT_SOURCE_DIR}/..)

# setup tensorflow libraries by python
if(USE_TF_PYTHON_LIBS)
  if(NOT "$ENV{CIBUILDWHEEL}" STREQUAL "1")
    find_package(
      Python
      COMPONENTS Interpreter Development
      REQUIRED)
  else()
    set(Python_LIBRARIES ${Python_LIBRARY})
    set(PYTHON_INCLUDE_DIRS ${PYTHON_INCLUDE_DIR})
  endif()
endif(USE_TF_PYTHON_LIBS)

# find tensorflow, I need tf abi info
if(NOT MDPU_C_ROOT)
  find_package(tensorflow REQUIRED)
endif()

# find threads
find_package(Threads)

# define build type
if((NOT DEFINED CMAKE_BUILD_TYPE) OR CMAKE_BUILD_TYPE STREQUAL "")
  set(CMAKE_BUILD_TYPE release)
endif()

# set op prec
set(HIGH_PREC_DEF "HIGH_PREC")
# this defination doesn't work, but leaving it empty will cause error
set(LOW_PREC_DEF "LOW_PREC")
set(HIGH_PREC_VARIANT "")
set(LOW_PREC_VARIANT "_low")

# find openmp
find_package(OpenMP)
if(OPENMP_FOUND)
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()

# optimize flags
option(ENABLE_NATIVE_OPTIMIZATION "Enable native optimization" OFF)
if(ENABLE_NATIVE_OPTIMIZATION)
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -march=native -mtune=native")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native -mtune=native")
endif()

# define names of libs
set(LIB_MDPU "mdpukit")
set(LIB_MDPU_OP "mdpukit_op")
if(BUILD_CPP_IF)
  set(LIB_MDPU_CC "mdpukit_cc")
  set(LIB_MDPU_C "mdpukit_c")
  if(USE_CUDA_TOOLKIT)
    set(LIB_MDPU_OP_DEVICE "mdpukit_op_cuda")
  elseif(USE_ROCM_TOOLKIT)
    set(LIB_MDPU_OP_DEVICE "mdpukit_op_rocm")
  else()
    set(LIB_MDPU_OP_DEVICE "mdpukit_op")
  endif()
  if(CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL 4.8)
    set(LIB_MDPU_NATIVE "mdpukit_native_md")
    set(LIB_MDPU_GROMACS "mdpukit_gromacs")
  else()
    message(
      STATUS
        "Your gcc/g++ version is ${CMAKE_CXX_COMPILER_VERSION}, so native MD is disabled. To enable them, use gcc/g++ >= 4.8."
    )
  endif()
endif(BUILD_CPP_IF)

option(DP_USING_C_API "Build third-party interface with C API" ON)

if(MDPU_C_ROOT)
  # find c library
  find_path(
    MDPU_INCLUDE_C_DIR mdpukit/mdpukit.hpp mdpukit/c_api.h
    HINTS ${MDPU_C_ROOT}
    PATH_SUFFIXES "include")
  find_library(
    mdpukit_c
    NAMES mdpukit_c
    HINTS ${MDPU_C_ROOT}
    PATH_SUFFIXES "lib")
  include(FindPackageHandleStandardArgs)
  find_package_handle_standard_args(MDPU_C DEFAULT_MSG mdpukit_c
                                    MDPU_INCLUDE_C_DIR)
  if(NOT MDPU_C_FOUND)
    message(
      FATAL_ERROR
        "mdpu-kit C library not found."
    )
  endif()

  add_library(${LIB_MDPU_C} SHARED IMPORTED GLOBAL)
  set_target_properties(
    ${LIB_MDPU_C}
    PROPERTIES IMPORTED_LINK_INTERFACE_LANGUAGES "C"
               IMPORTED_LOCATION "${mdpukit_c}"
               INTERFACE_INCLUDE_DIRECTORIES "${MDPU_INCLUDE_C_DIR}/mdpukit")
  # use variable for TF path to set mdpukit_c path
  set(TensorFlow_LIBRARY_PATH "${MDPU_C_ROOT}/lib")
  set(TENSORFLOW_INCLUDE_DIRS "${MDPU_C_ROOT}/include")
endif()

if(NOT MDPU_C_ROOT)
  add_subdirectory(op/)
  add_subdirectory(lib/)
endif()
if(BUILD_PY_IF)
  add_subdirectory(config/)
  # add_subdirectory (tests/)
endif(BUILD_PY_IF)
if(BUILD_CPP_IF)
  if(NOT MDPU_C_ROOT)
    add_subdirectory(api_cc/)
    add_subdirectory(api_c/)
  endif()
  if(LAMMPS_VERSION OR NOT BUILD_PY_IF)
    add_subdirectory(lmp/)
  endif()
  if(CMAKE_CXX_COMPILER_VERSION VERSION_GREATER 4.8)
    if(NOT BUILD_PY_IF)
      add_subdirectory(gmx/)
    endif()
  endif()
  if(BUILD_NODEJS_IF)
    add_subdirectory(nodejs/)
  endif()
endif(BUILD_CPP_IF)

# uninstall target
configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
  "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake" IMMEDIATE @ONLY)

add_custom_target(
  uninstall COMMAND ${CMAKE_COMMAND} -P
                    ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake)

# lammps target
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_lammps.cmake.in"
               "${CMAKE_CURRENT_BINARY_DIR}/cmake_lammps.cmake" IMMEDIATE @ONLY)

add_custom_target(lammps COMMAND ${CMAKE_COMMAND} -P
                                 ${CMAKE_CURRENT_BINARY_DIR}/cmake_lammps.cmake)

# add configure file
if(BUILD_CPP_IF
   AND NOT BUILD_PY_IF
   AND NOT MDPU_C_ROOT)
  include(CMakePackageConfigHelpers)
  set(targets_export_name
      ${CMAKE_PROJECT_NAME}Targets
      CACHE INTERNAL "")
  set(generated_dir
      "${CMAKE_CURRENT_BINARY_DIR}/generated"
      CACHE INTERNAL "")
  set(cmake_files_install_dir
      "${CMAKE_INSTALL_PREFIX}/lib/cmake/${CMAKE_PROJECT_NAME}")
  set(version_file "${generated_dir}/${CMAKE_PROJECT_NAME}ConfigVersion.cmake")
  write_basic_package_version_file(
    ${version_file}
    VERSION $<IF:${GIT_SUMM}?${GIT_SUMM}:"0.0.0">
    COMPATIBILITY AnyNewerVersion)
  install(
    EXPORT ${targets_export_name}
    NAMESPACE ${CMAKE_PROJECT_NAME}::
    DESTINATION ${cmake_files_install_dir})
  set(config_file "${generated_dir}/${CMAKE_PROJECT_NAME}Config.cmake")
  configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Config.cmake.in" "${config_file}"
    INSTALL_DESTINATION ${cmake_files_install_dir})
  install(FILES ${version_file} ${config_file}
          DESTINATION ${cmake_files_install_dir})
endif(
  BUILD_CPP_IF
  AND NOT BUILD_PY_IF
  AND NOT MDPU_C_ROOT)
