#!/usr/bin/env python3

# SPDX-License-Identifier: LGPL-3.0-or-later
from tensorflow.python.framework import (
    ops,
)

from mdpukit.env import (
    op_module,
)


@ops.RegisterGradient("AddFltMdpu")
def _AddFltMdpuGrad(op, grad):
    dx = op_module.flt_mdpu(grad)
    dw = dx
    return [dx, dw]
