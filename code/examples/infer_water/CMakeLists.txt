cmake_minimum_required(VERSION 3.7)
project(infer_water)

# find mdpu-kit
find_package(mdpu REQUIRED)

# C++ example
add_executable(infer_water_cc infer_water.cpp)
# link mdpu-kit C++ API
target_link_libraries(infer_water_cc PRIVATE mdpu::_cc)

# C example
add_executable(infer_water_c infer_water.c)
# link mdpu-kit C API
target_link_libraries(infer_water_c PRIVATE mdpu::_c)

# header-only example
add_executable(infer_water_hpp infer_water_hpp.cpp)
# link mdpu-kit C API
target_link_libraries(infer_water_hpp PRIVATE mdpu::_c)

# nlist
add_executable(infer_water_nlist infer_water_nlist.cpp)
# link mdpu-kit C API
target_link_libraries(infer_water_nlist PRIVATE mdpu::_c)
