// SPDX-License-Identifier: LGPL-3.0-or-later
#include <string>

#include "DataModifier.h"
#include "DeepPot.h"
#include "DeepTensor.h"
#include "neighbor_list.h"

// catch mdpu::mdpu_exception and store it in dp->exception
// return nothing
#define DP_REQUIRES_OK(dp, xx)              \
  try {                                     \
    xx;                                     \
  } catch (mdpu::mdpu_exception & ex) { \
    dp->exception = std::string(ex.what()); \
    return;                                 \
  }

#define DP_NEW_OK(dpcls, xx)                     \
  try {                                          \
    xx;                                          \
  } catch (mdpu::mdpu_exception & ex) {      \
    dpcls* _new_dp = new dpcls;                  \
    _new_dp->exception = std::string(ex.what()); \
    return _new_dp;                              \
  }

struct DP_Nlist {
  DP_Nlist();
  DP_Nlist(mdpu::InputNlist& nl);

  mdpu::InputNlist nl;
  std::string exception;
};

struct DP_DeepPot {
  DP_DeepPot();
  DP_DeepPot(mdpu::DeepPot& dp);

  mdpu::DeepPot dp;
  std::string exception;
  int dfparam;
  int daparam;
};

struct DP_DeepPotModelDevi {
  DP_DeepPotModelDevi();
  DP_DeepPotModelDevi(mdpu::DeepPotModelDevi& dp);

  mdpu::DeepPotModelDevi dp;
  std::string exception;
  int dfparam;
  int daparam;
};

struct DP_DeepTensor {
  DP_DeepTensor();
  DP_DeepTensor(mdpu::DeepTensor& dt);

  mdpu::DeepTensor dt;
  std::string exception;
};

struct DP_DipoleChargeModifier {
  DP_DipoleChargeModifier();
  DP_DipoleChargeModifier(mdpu::DipoleChargeModifier& dcm);

  mdpu::DipoleChargeModifier dcm;
  std::string exception;
};
