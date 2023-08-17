# SPDX-License-Identifier: LGPL-3.0-or-later
"""Test trained mdpu model."""
import logging
from pathlib import (
    Path,
)
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
    Tuple,
)

import numpy as np

from mdpukit import (
    DeepPotential,
)
from mdpukit.common import (
    expand_sys_str,
)
from mdpukit.utils import random as dp_random
from mdpukit.utils.data import (
    MDPUData,
)
from mdpukit.utils.weight_avg import (
    weighted_average,
)

if TYPE_CHECKING:
    from mdpukit.infer import (
        DeepPot,
    )
    from mdpukit.infer.deep_tensor import (
        DeepTensor,
    )

__all__ = ["test"]

log = logging.getLogger(__name__)


def test(
    *,
    model: str,
    system: str,
    datafile: str,
    set_prefix: str,
    numb_test: int,
    rand_seed: Optional[int],
    shuffle_test: bool,
    detail_file: str,
    atomic: bool,
    **kwargs,
):
    """Test model predictions.

    Parameters
    ----------
    model : str
        path where model is stored
    system : str
        system directory
    datafile : str
        the path to the list of systems to test
    set_prefix : str
        string prefix of set
    numb_test : int
        munber of tests to do
    rand_seed : Optional[int]
        seed for random generator
    shuffle_test : bool
        whether to shuffle tests
    detail_file : Optional[str]
        file where test details will be output
    atomic : bool
        whether per atom quantities should be computed
    **kwargs
        additional arguments

    Raises
    ------
    RuntimeError
        if no valid system was found
    """
    if datafile is not None:
        datalist = open(datafile)
        all_sys = datalist.read().splitlines()
        datalist.close()
    else:
        all_sys = expand_sys_str(system)

    if len(all_sys) == 0:
        raise RuntimeError("Did not find valid system")
    err_coll = []
    siz_coll = []

    # init random seed
    if rand_seed is not None:
        dp_random.seed(rand_seed % (2**32))

    # init model
    dp = DeepPotential(model)

    for cc, system in enumerate(all_sys):
        log.info("# ---------------output of dp test--------------- ")
        log.info(f"# testing system : {system}")

        # create data class
        tmap = dp.get_type_map() if dp.model_type == "ener" else None
        data = MDPUData(system, set_prefix, shuffle_test=shuffle_test, type_map=tmap)

        if dp.model_type == "ener":
            err = test_ener(
                dp,
                data,
                system,
                numb_test,
                detail_file,
                atomic,
                append_detail=(cc != 0),
            )
        log.info("# ----------------------------------------------- ")
        err_coll.append(err)

    avg_err = weighted_average(err_coll)

    if len(all_sys) != len(err_coll):
        log.warning("Not all systems are tested! Check if the systems are valid")

    if len(all_sys) > 1:
        log.info("# ----------weighted average of errors----------- ")
        log.info(f"# number of systems : {len(all_sys)}")
        if dp.model_type == "ener":
            print_ener_sys_avg(avg_err)
        log.info("# ----------------------------------------------- ")


def mae(diff: np.ndarray) -> float:
    """Calcalte mean absulote error.

    Parameters
    ----------
    diff : np.ndarray
        difference

    Returns
    -------
    float
        mean absulote error
    """
    return np.mean(np.abs(diff))


def rmse(diff: np.ndarray) -> float:
    """Calculate root mean square error.

    Parameters
    ----------
    diff : np.ndarray
        difference

    Returns
    -------
    float
        root mean square error
    """
    return np.sqrt(np.average(diff * diff))


def save_txt_file(
    fname: Path, data: np.ndarray, header: str = "", append: bool = False
):
    """Save numpy array to test file.

    Parameters
    ----------
    fname : str
        filename
    data : np.ndarray
        data to save to disk
    header : str, optional
        header string to use in file, by default ""
    append : bool, optional
        if true file will be appended insted of overwriting, by default False
    """
    flags = "ab" if append else "w"
    with fname.open(flags) as fp:
        np.savetxt(fp, data, header=header)


def test_ener(
    dp: "DeepPot",
    data: MDPUData,
    system: str,
    numb_test: int,
    detail_file: Optional[str],
    has_atom_ener: bool,
    append_detail: bool = False,
) -> Tuple[List[np.ndarray], List[int]]:
    """Test energy type model.

    Parameters
    ----------
    dp : DeepPot
        instance of deep potential
    data : MDPUData
        data container object
    system : str
        system directory
    numb_test : int
        munber of tests to do
    detail_file : Optional[str]
        file where test details will be output
    has_atom_ener : bool
        whether per atom quantities should be computed
    append_detail : bool, optional
        if true append output detail file, by default False

    Returns
    -------
    Tuple[List[np.ndarray], List[int]]
        arrays with results and their shapes
    """
    data.add("energy", 1, atomic=False, must=False, high_prec=True)
    data.add("force", 3, atomic=True, must=False, high_prec=False)
    data.add("virial", 9, atomic=False, must=False, high_prec=False)
    if dp.has_efield:
        data.add("efield", 3, atomic=True, must=True, high_prec=False)
    if has_atom_ener:
        data.add("atom_ener", 1, atomic=True, must=True, high_prec=False)
    if dp.get_dim_fparam() > 0:
        data.add(
            "fparam", dp.get_dim_fparam(), atomic=False, must=True, high_prec=False
        )
    if dp.get_dim_aparam() > 0:
        data.add("aparam", dp.get_dim_aparam(), atomic=True, must=True, high_prec=False)

    test_data = data.get_test()
    mixed_type = data.mixed_type
    natoms = len(test_data["type"][0])
    nframes = test_data["box"].shape[0]
    numb_test = min(nframes, numb_test)

    coord = test_data["coord"][:numb_test].reshape([numb_test, -1])
    box = test_data["box"][:numb_test]
    if dp.has_efield:
        efield = test_data["efield"][:numb_test].reshape([numb_test, -1])
    else:
        efield = None
    if not data.pbc:
        box = None
    if mixed_type:
        atype = test_data["type"][:numb_test].reshape([numb_test, -1])
    else:
        atype = test_data["type"][0]
    if dp.get_dim_fparam() > 0:
        fparam = test_data["fparam"][:numb_test]
    else:
        fparam = None
    if dp.get_dim_aparam() > 0:
        aparam = test_data["aparam"][:numb_test]
    else:
        aparam = None

    ret = dp.eval(
        coord,
        box,
        atype,
        fparam=fparam,
        aparam=aparam,
        atomic=has_atom_ener,
        efield=efield,
        mixed_type=mixed_type,
    )
    energy = ret[0]
    force = ret[1]
    virial = ret[2]
    energy = energy.reshape([numb_test, 1])
    force = force.reshape([numb_test, -1])
    virial = virial.reshape([numb_test, 9])
    if has_atom_ener:
        ae = ret[3]
        av = ret[4]
        ae = ae.reshape([numb_test, -1])
        av = av.reshape([numb_test, -1])
    if dp.get_ntypes_spin() != 0:
        ntypes_real = dp.get_ntypes() - dp.get_ntypes_spin()
        nloc = natoms
        nloc_real = sum([np.count_nonzero(atype == ii) for ii in range(ntypes_real)])
        force_r = np.split(
            force, indices_or_sections=[nloc_real * 3, nloc * 3], axis=1
        )[0]
        force_m = np.split(
            force, indices_or_sections=[nloc_real * 3, nloc * 3], axis=1
        )[1]
        test_force_r = np.split(
            test_data["force"][:numb_test],
            indices_or_sections=[nloc_real * 3, nloc * 3],
            axis=1,
        )[0]
        test_force_m = np.split(
            test_data["force"][:numb_test],
            indices_or_sections=[nloc_real * 3, nloc * 3],
            axis=1,
        )[1]

    diff_e = energy - test_data["energy"][:numb_test].reshape([-1, 1])
    mae_e = mae(diff_e)
    rmse_e = rmse(diff_e)
    diff_f = force - test_data["force"][:numb_test]
    mae_f = mae(diff_f)
    rmse_f = rmse(diff_f)
    diff_v = virial - test_data["virial"][:numb_test]
    mae_v = mae(diff_v)
    rmse_v = rmse(diff_v)
    mae_ea = mae_e / natoms
    rmse_ea = rmse_e / natoms
    mae_va = mae_v / natoms
    rmse_va = rmse_v / natoms
    if has_atom_ener:
        diff_ae = test_data["atom_ener"][:numb_test].reshape([-1]) - ae.reshape([-1])
        mae_ae = mae(diff_ae)
        rmse_ae = rmse(diff_ae)
    if dp.get_ntypes_spin() != 0:
        mae_fr = mae(force_r - test_force_r)
        mae_fm = mae(force_m - test_force_m)
        rmse_fr = rmse(force_r - test_force_r)
        rmse_fm = rmse(force_m - test_force_m)

    log.info(f"# number of test data : {numb_test:d} ")
    log.info(f"Energy MAE         : {mae_e:e} eV")
    log.info(f"Energy RMSE        : {rmse_e:e} eV")
    log.info(f"Energy MAE/Natoms  : {mae_ea:e} eV")
    log.info(f"Energy RMSE/Natoms : {rmse_ea:e} eV")
    if dp.get_ntypes_spin() == 0:
        log.info(f"Force  MAE         : {mae_f:e} eV/A")
        log.info(f"Force  RMSE        : {rmse_f:e} eV/A")
    else:
        log.info(f"Force atom MAE      : {mae_fr:e} eV/A")
        log.info(f"Force spin MAE      : {mae_fm:e} eV/uB")
        log.info(f"Force atom RMSE     : {rmse_fr:e} eV/A")
        log.info(f"Force spin RMSE     : {rmse_fm:e} eV/uB")

    if data.pbc:
        log.info(f"Virial MAE         : {mae_v:e} eV")
        log.info(f"Virial RMSE        : {rmse_v:e} eV")
        log.info(f"Virial MAE/Natoms  : {mae_va:e} eV")
        log.info(f"Virial RMSE/Natoms : {rmse_va:e} eV")
    if has_atom_ener:
        log.info(f"Atomic ener MAE    : {mae_ae:e} eV")
        log.info(f"Atomic ener RMSE   : {rmse_ae:e} eV")

    if detail_file is not None:
        detail_path = Path(detail_file)

        pe = np.concatenate(
            (
                np.reshape(test_data["energy"][:numb_test], [-1, 1]),
                np.reshape(energy, [-1, 1]),
            ),
            axis=1,
        )
        save_txt_file(
            detail_path.with_suffix(".e.out"),
            pe,
            header="%s: data_e pred_e" % system,
            append=append_detail,
        )
        pe_atom = pe / natoms
        save_txt_file(
            detail_path.with_suffix(".e_peratom.out"),
            pe_atom,
            header="%s: data_e pred_e" % system,
            append=append_detail,
        )
        if dp.get_ntypes_spin() == 0:
            pf = np.concatenate(
                (
                    np.reshape(test_data["force"][:numb_test], [-1, 3]),
                    np.reshape(force, [-1, 3]),
                ),
                axis=1,
            )
            save_txt_file(
                detail_path.with_suffix(".f.out"),
                pf,
                header="%s: data_fx data_fy data_fz pred_fx pred_fy pred_fz" % system,
                append=append_detail,
            )
        else:
            pf_real = np.concatenate(
                (np.reshape(test_force_r, [-1, 3]), np.reshape(force_r, [-1, 3])),
                axis=1,
            )
            pf_mag = np.concatenate(
                (np.reshape(test_force_m, [-1, 3]), np.reshape(force_m, [-1, 3])),
                axis=1,
            )
            save_txt_file(
                detail_path.with_suffix(".fr.out"),
                pf_real,
                header="%s: data_fx data_fy data_fz pred_fx pred_fy pred_fz" % system,
                append=append_detail,
            )
            save_txt_file(
                detail_path.with_suffix(".fm.out"),
                pf_mag,
                header="%s: data_fmx data_fmy data_fmz pred_fmx pred_fmy pred_fmz"
                % system,
                append=append_detail,
            )
        pv = np.concatenate(
            (
                np.reshape(test_data["virial"][:numb_test], [-1, 9]),
                np.reshape(virial, [-1, 9]),
            ),
            axis=1,
        )
        save_txt_file(
            detail_path.with_suffix(".v.out"),
            pv,
            header=f"{system}: data_vxx data_vxy data_vxz data_vyx data_vyy "
            "data_vyz data_vzx data_vzy data_vzz pred_vxx pred_vxy pred_vxz pred_vyx "
            "pred_vyy pred_vyz pred_vzx pred_vzy pred_vzz",
            append=append_detail,
        )
        pv_atom = pv / natoms
        save_txt_file(
            detail_path.with_suffix(".v_peratom.out"),
            pv_atom,
            header=f"{system}: data_vxx data_vxy data_vxz data_vyx data_vyy "
            "data_vyz data_vzx data_vzy data_vzz pred_vxx pred_vxy pred_vxz pred_vyx "
            "pred_vyy pred_vyz pred_vzx pred_vzy pred_vzz",
            append=append_detail,
        )
    if dp.get_ntypes_spin() == 0:
        return {
            "mae_e": (mae_e, energy.size),
            "mae_ea": (mae_ea, energy.size),
            "mae_f": (mae_f, force.size),
            "mae_v": (mae_v, virial.size),
            "mae_va": (mae_va, virial.size),
            "rmse_e": (rmse_e, energy.size),
            "rmse_ea": (rmse_ea, energy.size),
            "rmse_f": (rmse_f, force.size),
            "rmse_v": (rmse_v, virial.size),
            "rmse_va": (rmse_va, virial.size),
        }
    else:
        return {
            "mae_e": (mae_e, energy.size),
            "mae_ea": (mae_ea, energy.size),
            "mae_fr": (mae_fr, force_r.size),
            "mae_fm": (mae_fm, force_m.size),
            "mae_v": (mae_v, virial.size),
            "mae_va": (mae_va, virial.size),
            "rmse_e": (rmse_e, energy.size),
            "rmse_ea": (rmse_ea, energy.size),
            "rmse_fr": (rmse_fr, force_r.size),
            "rmse_fm": (rmse_fm, force_m.size),
            "rmse_v": (rmse_v, virial.size),
            "rmse_va": (rmse_va, virial.size),
        }


def print_ener_sys_avg(avg: Dict[str, float]):
    """Print errors summary for energy type potential.

    Parameters
    ----------
    avg : np.ndarray
        array with summaries
    """
    log.info(f"Energy MAE         : {avg['mae_e']:e} eV")
    log.info(f"Energy RMSE        : {avg['rmse_e']:e} eV")
    log.info(f"Energy MAE/Natoms  : {avg['mae_ea']:e} eV")
    log.info(f"Energy RMSE/Natoms : {avg['rmse_ea']:e} eV")
    if "rmse_f" in avg.keys():
        log.info(f"Force  MAE         : {avg['mae_f']:e} eV/A")
        log.info(f"Force  RMSE        : {avg['rmse_f']:e} eV/A")
    else:
        log.info(f"Force atom MAE      : {avg['mae_fr']:e} eV/A")
        log.info(f"Force spin MAE      : {avg['mae_fm']:e} eV/uB")
        log.info(f"Force atom RMSE     : {avg['rmse_fr']:e} eV/A")
        log.info(f"Force spin RMSE     : {avg['rmse_fm']:e} eV/uB")
    log.info(f"Virial MAE         : {avg['mae_v']:e} eV")
    log.info(f"Virial RMSE        : {avg['rmse_v']:e} eV")
    log.info(f"Virial MAE/Natoms  : {avg['mae_va']:e} eV")
    log.info(f"Virial RMSE/Natoms : {avg['rmse_va']:e} eV")


def run_test(dp: "DeepTensor", test_data: dict, numb_test: int, test_sys: MDPUData):
    """Run tests.

    Parameters
    ----------
    dp : DeepTensor
        instance of deep potential
    test_data : dict
        dictionary with test data
    numb_test : int
        munber of tests to do
    test_sys : MDPUData
        test system

    Returns
    -------
    [type]
        [description]
    """
    nframes = test_data["box"].shape[0]
    numb_test = min(nframes, numb_test)

    coord = test_data["coord"][:numb_test].reshape([numb_test, -1])
    if test_sys.pbc:
        box = test_data["box"][:numb_test]
    else:
        box = None
    atype = test_data["type"][0]
    prediction = dp.eval(coord, box, atype)

    return prediction.reshape([numb_test, -1]), numb_test, atype

