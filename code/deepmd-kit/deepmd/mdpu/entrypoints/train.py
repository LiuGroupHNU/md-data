# SPDX-License-Identifier: LGPL-3.0-or-later
import logging
import os
from typing import (
    Optional,
)

from deepmd.entrypoints.freeze import (
    freeze,
)
from deepmd.entrypoints.train import (
    train,
)
from deepmd.env import (
    tf,
)
from deepmd.mdpu.data.data import (
    jdata_deepmd_input_v0,
)
from deepmd.mdpu.entrypoints.mapt import (
    mapt,
)
from deepmd.mdpu.entrypoints.wrap import (
    wrap,
)
from deepmd.mdpu.utils.config import (
    mdpu_cfg,
)
from deepmd.mdpu.utils.fio import (
    FioDic,
)

log = logging.getLogger(__name__)

jdata_cmd_train = {
    "INPUT": "train.json",
    "init_model": None,
    "restart": None,
    "output": "out.json",
    "init_frz_model": None,
    "mpi_log": "master",
    "log_level": 2,
    "log_path": "train.log",
    "is_compress": False,
}

jdata_cmd_freeze = {
    "checkpoint_folder": ".",
    "output": "frozen_model.pb",
    "node_names": None,
    "mdpu_weight": "mdpu/weight.npy",
}


def normalized_input(fn, PATH_CNN, CONFIG_CNN):
    r"""Normalize a input script file for continuous neural network."""
    f = FioDic()
    jdata = f.load(fn, jdata_deepmd_input_v0)
    # mdpu
    jdata_mdpu = jdata_deepmd_input_v0["mdpu"]
    jdata_mdpu["enable"] = True
    jdata_mdpu["config_file"] = CONFIG_CNN
    jdata_mdpu_ = f.get(jdata, "mdpu", jdata_mdpu)
    jdata_mdpu = f.update(jdata_mdpu_, jdata_mdpu)
    # model
    jdata_model = {
        "descriptor": {
            "seed": 1,
            "sel": jdata_mdpu_["sel"],
            "rcut": jdata_mdpu_["rcut"],
            "rcut_smth": jdata_mdpu_["rcut_smth"],
        },
        "fitting_net": {"seed": 1},
        "type_map": [],
    }
    jdata_model["type_map"] = f.get(jdata_mdpu_, "type_map", [])
    mdpu_cfg.init_from_jdata(jdata_mdpu)
    mdpu_cfg.init_from_deepmd_input(jdata_model)
    mdpu_cfg.init_train_mode("cnn")
    # training
    jdata_train = f.get(jdata, "training", {})
    jdata_train["disp_training"] = True
    jdata_train["time_training"] = True
    jdata_train["profiling"] = False
    jdata_train["disp_file"] = os.path.join(
        PATH_CNN, os.path.split(jdata_train["disp_file"])[1]
    )
    jdata_train["save_ckpt"] = os.path.join(
        PATH_CNN, os.path.split(jdata_train["save_ckpt"])[1]
    )
    #
    jdata["model"] = mdpu_cfg.get_model_jdata()
    jdata["mdpu"] = mdpu_cfg.get_mdpu_jdata()
    return jdata


def normalized_input_qnn(jdata, PATH_QNN, CONFIG_CNN, WEIGHT_CNN, MAP_CNN):
    r"""Normalize a input script file for quantize neural network."""
    #
    jdata_mdpu = jdata_deepmd_input_v0["mdpu"]
    jdata_mdpu["enable"] = True
    jdata_mdpu["version"] = mdpu_cfg.version
    jdata_mdpu["config_file"] = CONFIG_CNN
    jdata_mdpu["weight_file"] = WEIGHT_CNN
    jdata_mdpu["map_file"] = MAP_CNN
    mdpu_cfg.init_from_jdata(jdata_mdpu)
    mdpu_cfg.init_train_mode("qnn")
    jdata["mdpu"] = mdpu_cfg.get_mdpu_jdata()
    # training
    jdata2 = jdata["training"]
    jdata2["disp_file"] = os.path.join(PATH_QNN, os.path.split(jdata2["disp_file"])[1])
    jdata2["save_ckpt"] = os.path.join(PATH_QNN, os.path.split(jdata2["save_ckpt"])[1])
    jdata["training"] = jdata2
    return jdata


def train_mdpu(
    *,
    INPUT: str,
    restart: Optional[str],
    step: str,
    skip_neighbor_stat: bool = False,
    **kwargs,
):
    # test input
    if not os.path.exists(INPUT):
        log.warning("The input script %s does not exist" % (INPUT))
    # STEP1
    PATH_CNN = "mdpu_cnn"
    CONFIG_CNN = os.path.join(PATH_CNN, "config.npy")
    INPUT_CNN = os.path.join(PATH_CNN, "train.json")
    WEIGHT_CNN = os.path.join(PATH_CNN, "weight.npy")
    FRZ_MODEL_CNN = os.path.join(PATH_CNN, "frozen_model.pb")
    MAP_CNN = os.path.join(PATH_CNN, "map.npy")
    LOG_CNN = os.path.join(PATH_CNN, "train.log")
    if step == "s1":
        # normailize input file
        jdata = normalized_input(INPUT, PATH_CNN, CONFIG_CNN)
        FioDic().save(INPUT_CNN, jdata)
        mdpu_cfg.save(CONFIG_CNN)
        # train cnn
        jdata = jdata_cmd_train.copy()
        jdata["INPUT"] = INPUT_CNN
        jdata["log_path"] = LOG_CNN
        jdata["restart"] = restart
        jdata["skip_neighbor_stat"] = skip_neighbor_stat
        train(**jdata)
        tf.reset_default_graph()
        # freeze
        jdata = jdata_cmd_freeze.copy()
        jdata["checkpoint_folder"] = PATH_CNN
        jdata["output"] = FRZ_MODEL_CNN
        jdata["mdpu_weight"] = WEIGHT_CNN
        freeze(**jdata)
        tf.reset_default_graph()
        # map table
        jdata = {
            "mdpu_config": CONFIG_CNN,
            "mdpu_weight": WEIGHT_CNN,
            "mdpu_map": MAP_CNN,
        }
        mapt(**jdata)
        tf.reset_default_graph()
    # STEP2
    PATH_QNN = "mdpu_qnn"
    CONFIG_QNN = os.path.join(PATH_QNN, "config.npy")
    INPUT_QNN = os.path.join(PATH_QNN, "train.json")
    WEIGHT_QNN = os.path.join(PATH_QNN, "weight.npy")
    FRZ_MODEL_QNN = os.path.join(PATH_QNN, "frozen_model.pb")
    MODEL_QNN = os.path.join(PATH_QNN, "model.pb")
    LOG_QNN = os.path.join(PATH_QNN, "train.log")

    if step == "s2":
        # normailize input file
        jdata = normalized_input(INPUT, PATH_CNN, CONFIG_CNN)
        jdata = normalized_input_qnn(jdata, PATH_QNN, CONFIG_CNN, WEIGHT_CNN, MAP_CNN)
        FioDic().save(INPUT_QNN, jdata)
        mdpu_cfg.save(CONFIG_QNN)
        # train qnn
        jdata = jdata_cmd_train.copy()
        jdata["INPUT"] = INPUT_QNN
        jdata["log_path"] = LOG_QNN
        jdata["skip_neighbor_stat"] = skip_neighbor_stat
        train(**jdata)
        tf.reset_default_graph()
        # freeze
        jdata = jdata_cmd_freeze.copy()
        jdata["checkpoint_folder"] = PATH_QNN
        jdata["output"] = FRZ_MODEL_QNN
        jdata["mdpu_weight"] = WEIGHT_QNN
        freeze(**jdata)
        tf.reset_default_graph()
        # wrap
        jdata = {
            "mdpu_config": CONFIG_QNN,
            "mdpu_weight": WEIGHT_QNN,
            "mdpu_map": MAP_CNN,
            "mdpu_model": MODEL_QNN,
        }
        wrap(**jdata)
        tf.reset_default_graph()
