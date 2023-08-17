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

#include "DeepPot.h"
#include "errors.h"
TEST(TestMDPUException, mdpuexception) {
  std::string expected_error_message = "mdpu-kit Error: unittest";
  try {
    throw mdpu::mdpu_exception("unittest");
  } catch (mdpu::mdpu_exception &ex) {
    EXPECT_STREQ(expected_error_message.c_str(), ex.what());
  }
}

TEST(TestMDPUException, mdpuexception_nofile) {
  ASSERT_THROW(mdpu::DeepPot("_no_such_file.pb"), mdpu::mdpu_exception);
}
