# SPDX-License-Identifier: LGPL-3.0-or-later
"""Submodule containing all the implemented potentials."""

from pathlib import (
    Path,
)
from typing import (
    Union,
)

from .deep_eval import (
    DeepEval,
)
from .deep_pot import (
    DeepPot,
)
from .model_devi import (
    calc_model_devi,
)

__all__ = [
    "DeepPotential",
    "DeepEval",
    "DeepPot",
    "calc_model_devi",
]


def DeepPotential(
    model_file: Union[str, Path],
    load_prefix: str = "load",
    default_tf_graph: bool = False,
) -> Union[DeepPot]:
    """Factory function that will inialize appropriate potential read from `model_file`.

    Parameters
    ----------
    model_file : str
        The name of the frozen model file.
    load_prefix : str
        The prefix in the load computational graph
    default_tf_graph : bool
        If uses the default tf graph, otherwise build a new tf graph for evaluation

    Returns
    -------
    Union[DDeepPot]
        one of the available potentials

    Raises
    ------
    RuntimeError
        if model file does not correspond to any implementd potential
    """
    mf = Path(model_file)

    model_type = DeepEval(
        mf, load_prefix=load_prefix, default_tf_graph=default_tf_graph
    ).model_type

    if model_type == "ener":
        dp = DeepPot(mf, load_prefix=load_prefix, default_tf_graph=default_tf_graph)
    else:
        raise RuntimeError(f"unknown model type {model_type}")

    return dp
