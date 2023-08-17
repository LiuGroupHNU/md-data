// SPDX-License-Identifier: LGPL-3.0-or-later
#pragma once

#include <stdexcept>
#include <string>

namespace mdpu {
/**
 * @brief General mdpu-kit exception. Throw if anything doesn't work.
 **/
struct mdpu_exception : public std::runtime_error {
 public:
  mdpu_exception() : runtime_error("mdpu-kit Error!"){};
  mdpu_exception(const std::string& msg)
      : runtime_error(std::string("mdpu-kit Error: ") + msg){};
};

struct mdpu_exception_oom : public mdpu_exception {
 public:
  mdpu_exception_oom() : mdpu_exception("mdpu-kit OOM!"){};
  mdpu_exception_oom(const std::string& msg)
      : mdpu_exception(std::string("mdpu-kit OOM: ") + msg){};
};
};  // namespace mdpu
