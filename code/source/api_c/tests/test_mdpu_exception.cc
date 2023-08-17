// SPDX-License-Identifier: LGPL-3.0-or-later
#include <fcntl.h>
#include <gtest/gtest.h>
#include <sys/stat.h>
#include <sys/types.h>

#include <algorithm>
#include <cmath>
#include <fstream>
#include <string>
#include <vector>

#include "mdpu.hpp"

TEST(TestMDPUException, mdpuexception) {
  std::string expected_error_message = "mdpu-kit C API Error: unittest";
  try {
    throw mdpu::hpp::mdpu_exception("unittest");
  } catch (mdpu::hpp::mdpu_exception &ex) {
    EXPECT_STREQ(expected_error_message.c_str(), ex.what());
  }
}

TEST(TestMDPUException, mdpuexception_nofile) {
  ASSERT_THROW(mdpu::hpp::DeepPot("_no_such_file.pb"),
               mdpu::hpp::mdpu_exception);
}
