#!/usr/bin/env python3

# SPDX-License-Identifier: LGPL-3.0-or-later
from tensorflow.python.framework import (
    ops,
)

from deepmd.env import (
    op_module,
)


@ops.RegisterGradient("FltMdpu")
def _FltMdpuGrad(op, grad):
    dx = op_module.flt_mdpu(grad)
    return [dx]
