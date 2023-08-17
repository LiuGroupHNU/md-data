# SPDX-License-Identifier: LGPL-3.0-or-later
from deepmd.env import (
    GLOBAL_TF_FLOAT_PRECISION,
    tf,
)
from deepmd.mdpu.utils.config import (
    mdpu_cfg,
)
from deepmd.mdpu.utils.network import one_layer as one_layer_mdpu

__all__ = [
    "GLOBAL_TF_FLOAT_PRECISION",
    "tf",
    "mdpu_cfg",
    "one_layer_mdpu",
]
