
<span style="font-size:larger;">mdpu-kit Manual</span>
========

# Table of contents
- [mdpu-kit Manual](#mdpu-kit-manual)
- [Table of contents](#table-of-contents)
- [About mdpu-kit](#about-mdpu-kit)
  - [Highlighted features](#highlighted-features)
  - [License and credits](#license-and-credits)
- [Download and install](#download-and-install)
- [Use mdpu-kit](#use-mdpu-kit)
- [Advanced](#advanced)
- [Code structure](#code-structure)

# About mdpu-kit
mdpu-kit is a package written in Python/C++, designed to minimize the effort required to build deep learning-based model of interatomic potential energy and force field and to perform molecular dynamics (MD). This brings new hopes to addressing the accuracy-versus-efficiency dilemma in molecular simulations. Applications of mdpu-kit span from finite molecules to extended systems and from metallic systems to chemically bonded systems.


## Highlighted features
* **interfaced with TensorFlow**, one of the most popular deep learning frameworks, making the training process highly automatic and efficient, in addition, Tensorboard can be used to visualize training procedures.
* **interfaced with high-performance classical MD packages**, i.e., LAMMPS.
* **implements the Deep Potential series models**, which have been successfully applied to finite and extended systems including organic molecules, metals, semiconductors, insulators, etc.
* **implements MPI supports**, making it highly efficient for high-performance parallel and distributed computing.
* **highly modularized**, easy to adapt to different descriptors for deep learning-based potential energy models.

## License and credits
The project mdpu-kit is licensed under [GNU LGPLv3.0](./LICENSE).
If you use this code in any future publications, please cite the following publications for general purpose:
Breaking the Speed, Power, Cost and Size Limits of Molecular Dynamics with Ab Initio Accuracy # NATCOMPUTSCI-23-0729

In addition, please follow [the bib file](CITATIONS.bib) to cite the methods you used.

# Download and install
One may manually install mdpu-kit by following the instructions on [installing the Python interface](doc/install/install-from-source.md#install-the-python-interface) and [installing the C++ interface](doc/install/install-from-source.md#install-the-c-interface). The C++ interface is necessary when using mdpu-kit with LAMMPS.


# Use mdpu-kit

A quick start on using mdpu-kit can be found [here](doc/mdpu/mdpu.md).

# Advanced

- [Installation](doc/install/index.md)
    - [Install from source code](doc/install/install-from-source.md)
- [Data](doc/data/index.md)
    - [System](doc/data/system.md)
    - [Formats of a system](doc/data/data-conv.md)
    - [Prepare data with dpdata](doc/data/dpdata.md)
- Training
    - [Training a model](doc/mdpu/mdpu.md#training)
- Test
    - [Test a model](doc/mdpu/mdpu.md#testing)
- [Inference](doc/inference/index.rst)
    - [Python interface](doc/inference/python.md)
    - [C++ interface](doc/inference/cxx.md)
- [Integrate with third-party packages](doc/third-party/index.rst)
    - [Run MD with LAMMPS](doc/third-party/lammps.md)
    - [LAMMPS commands](doc/third-party/lammps-command.md)
- [Use MDPU](doc/mdpu/index.md)

# Code structure

The code is organized as follows:

* `data/raw`: tools manipulating the raw data files.
* `examples`: examples.
* `mdpukit`: mdpu-kit python modules.
* `source/api_cc`: source code of mdpu-kit C++ API.
* `source/lib`: source code of mdpu-kit library.
* `source/lmp`: source code of Lammps module.
* `source/op`: TensorFlow op implementation. working with the library.

