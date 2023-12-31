# SPDX-License-Identifier: LGPL-3.0-or-later
"""Setup script for mdpu-kit package."""

import os
import sys

from packaging.version import (
    Version,
)
from skbuild import (
    setup,
)
from wheel.bdist_wheel import (
    bdist_wheel,
)

topdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(topdir, "backend"))

from find_tensorflow import (
    find_tensorflow,
    get_tf_requirement,
    get_tf_version,
)

cmake_args = []
extra_scripts = []
# get variant option from the environment varibles, available: cpu, cuda, rocm
dp_variant = os.environ.get("DP_VARIANT", "cpu").lower()
if dp_variant == "cpu" or dp_variant == "":
    cmake_minimum_required_version = "3.16"
elif dp_variant == "cuda":
    cmake_minimum_required_version = "3.23"
    cmake_args.append("-DUSE_CUDA_TOOLKIT:BOOL=TRUE")
    cuda_root = os.environ.get("CUDAToolkit_ROOT")
    if cuda_root:
        cmake_args.append(f"-DCUDAToolkit_ROOT:STRING={cuda_root}")
elif dp_variant == "rocm":
    cmake_minimum_required_version = "3.21"
    cmake_args.append("-DUSE_ROCM_TOOLKIT:BOOL=TRUE")
    rocm_root = os.environ.get("ROCM_ROOT")
    if rocm_root:
        cmake_args.append(f"-DCMAKE_HIP_COMPILER_ROCM_ROOT:STRING={rocm_root}")
    hipcc_flags = os.environ.get("HIP_HIPCC_FLAGS")
    if hipcc_flags:
        cmake_args.append(f"-DHIP_HIPCC_FLAGS:STRING={hipcc_flags}")
else:
    raise RuntimeError("Unsupported DP_VARIANT option: %s" % dp_variant)

if os.environ.get("DP_BUILD_TESTING", "0") == "1":
    cmake_args.append("-DBUILD_TESTING:BOOL=TRUE")
if os.environ.get("DP_ENABLE_NATIVE_OPTIMIZATION", "0") == "1":
    cmake_args.append("-DENABLE_NATIVE_OPTIMIZATION:BOOL=TRUE")
dp_lammps_version = os.environ.get("DP_LAMMPS_VERSION", "")
if dp_lammps_version != "":
    cmake_args.append("-DBUILD_CPP_IF:BOOL=TRUE")
    cmake_args.append("-DUSE_TF_PYTHON_LIBS:BOOL=TRUE")
else:
    cmake_args.append("-DBUILD_CPP_IF:BOOL=FALSE")

if dp_lammps_version != "":
    cmake_args.append(f"-DLAMMPS_VERSION={dp_lammps_version}")


tf_install_dir, _ = find_tensorflow()
tf_version = get_tf_version(tf_install_dir)
if tf_version == "" or Version(tf_version) >= Version("2.12"):
    find_libpython_requires = []
else:
    find_libpython_requires = ["find_libpython"]
cmake_args.append(f"-DTENSORFLOW_VERSION={tf_version}")


class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()
        if python.startswith("cp"):
            if tf_version == "" or Version(tf_version) >= Version("2.12"):
                return "py38", "none", plat
            return "py37", "none", plat
        return python, abi, plat


# TODO: migrate packages and entry_points to pyproject.toml after scikit-build supports it
# See also https://scikit-build.readthedocs.io/en/latest/usage.html#setuptools-options
setup(
    packages=[
        "mdpukit",
        "mdpukit/descriptor",
        "mdpukit/fit",
        "mdpukit/infer",
        "mdpukit/loss",
        "mdpukit/utils",
        "mdpukit/loggers",
        "mdpukit/cluster",
        "mdpukit/entrypoints",
        "mdpukit/op",
        "mdpukit/model",
        "mdpukit/train",
        "mdpukit/mdpu",
        "mdpukit/mdpu/data",
        "mdpukit/mdpu/descriptor",
        "mdpukit/mdpu/entrypoints",
        "mdpukit/mdpu/fit",
        "mdpukit/mdpu/utils",
        "mdpukit_cli",
    ],
    cmake_args=[
        f"-DTENSORFLOW_ROOT:PATH={tf_install_dir}",
        "-DBUILD_PY_IF:BOOL=TRUE",
        *cmake_args,
    ],
    cmake_source_dir="source",
    cmake_minimum_required_version=cmake_minimum_required_version,
    extras_require={
        "test": ["dpdata>=0.1.9", "ase", "pytest", "pytest-cov", "pytest-sugar"],
        "docs": [
            "sphinx>=3.1.1",
            "sphinx_rtd_theme>=1.0.0rc1",
            "sphinx_markdown_tables",
            "myst-nb",
            "breathe",
            "exhale",
            "numpydoc",
            "ase",
            "deepmodeling-sphinx>=0.1.0",
            "dargs>=0.3.4",
            "sphinx-argparse",
            "pygments-lammps",
            "sphinxcontrib-bibtex",
        ],
        "lmp": [
            "lammps~=2022.6.23.4.0; platform_system=='Linux'",
            "lammps~=2022.6.23.4.0; platform_system!='Linux'",
            *find_libpython_requires,
        ],
        **get_tf_requirement(tf_version),
        "cu11": [
            "nvidia-cuda-runtime-cu11",
            "nvidia-cublas-cu11",
            "nvidia-cufft-cu11",
            "nvidia-curand-cu11",
            "nvidia-cusolver-cu11",
            "nvidia-cusparse-cu11",
            "nvidia-cudnn-cu11",
            "nvidia-cuda-nvcc-cu11",
        ],
        "cu12": [
            "nvidia-cuda-runtime-cu12",
            "nvidia-cublas-cu12",
            "nvidia-cufft-cu12",
            "nvidia-curand-cu12",
            "nvidia-cusolver-cu12",
            "nvidia-cusparse-cu12",
            "nvidia-cudnn-cu12",
            "nvidia-cuda-nvcc-cu12",
        ],
    },
    entry_points={
        "console_scripts": ["dp = mdpukit_cli.main:main", *extra_scripts],
        "lammps.plugins": ["mdpukit = mdpukit.lmp:get_op_dir"],
    },
    cmdclass={
        "bdist_wheel": bdist_wheel_abi3,
    },
)
