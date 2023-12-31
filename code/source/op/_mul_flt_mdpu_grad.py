#!/usr/bin/env python3

# SPDX-License-Identifier: LGPL-3.0-or-later
from tensorflow.python.framework import (
    ops,
)

from mdpukit.env import (
    op_module,
    tf,
)


@ops.RegisterGradient("MulFltMdpu")
def _MulFltMdpuGrad(op, grad):
    x = op.inputs[0]
    w = op.inputs[1]
    # transpose for 2-dimension and 3-dimension multiplication
    shx = x.shape.as_list()
    shw = w.shape.as_list()
    shx = [None if (d == -1) else d for d in shx]
    shw = [None if (d == -1) else d for d in shw]
    if shx[-1] == shw[-1]:
        dx = op_module.mul_flt_mdpu(w, grad)
        dw = op_module.mul_flt_mdpu(x, grad)
    else:
        # shx[-1] == 1, shw[-1] == M
        dx = op_module.dotmul_flt_mdpu(w, grad)
        dw = op_module.mul_flt_mdpu(x, grad)
    # add shapes
    dx = tf.ensure_shape(dx, shx)
    dw = tf.ensure_shape(dw, shw)
    return [dx, dw]
