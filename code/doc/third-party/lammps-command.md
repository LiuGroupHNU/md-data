# LAMMPS commands

## Enable mdpu-kit plugin (plugin mode)

If you are using the plugin mode, enable mdpu-kit package in LAMMPS with `plugin` command:

```lammps
plugin load libmdpu_lmp.so
```

After LAMMPS version `patch_24Mar2022`, another way to load plugins is to set the environmental variable `LAMMPS_PLUGIN_PATH`:

```sh
LAMMPS_PLUGIN_PATH=$mdpu_root/lib/mdpu_lmp
```

where `$mdpu_root` is the directory to [install C++ interface](../install/install-from-source.md).

The built-in mode doesn't need this step.

## pair_style `mdpu`

The mdpu-kit package provides the pair_style `mdpu`

```lammps
pair_style mdpu models ... keyword value ...
```
- mdpu = style of this pair_style
- models = frozen model(s) to compute the interaction.
If multiple models are provided, then only the first model serves to provide energy and force prediction for each timestep of molecular dynamics,
and the model deviation will be computed among all models every `out_freq` timesteps.
- keyword = *out_file* or *out_freq* or *fparam* or *fparam_from_compute* or *atomic* or *relative* or *relative_v* or *aparam* or *ttm*
<pre>
    <i>out_file</i> value = filename
        filename = The file name for the model deviation output. Default is model_devi.out
    <i>out_freq</i> value = freq
        freq = Frequency for the model deviation output. Default is 100.
    <i>fparam</i> value = parameters
        parameters = one or more frame parameters required for model evaluation.
    <i>fparam_from_compute</i> value = id
        id = compute id used to update the frame parameter.
    <i>atomic</i> = no value is required.
        If this keyword is set, the model deviation of each atom will be output.
    <i>relative</i> value = level
        level = The level parameter for computing the relative model deviation of the force
    <i>relative_v</i> value = level
        level = The level parameter for computing the relative model deviation of the virial
    <i>aparam</i> value = parameters
        parameters = one or more atomic parameters of each atom required for model evaluation
    <i>ttm</i> value = id
        id = fix ID of fix ttm
</pre>

### Examples
```lammps
pair_style mdpu graph.pb
pair_style mdpu graph.pb fparam 1.2
pair_style mdpu graph_0.pb graph_1.pb graph_2.pb out_file md.out out_freq 10 atomic relative 1.0
pair_coeff * * O H

pair_style mdpu cp.pb fparam_from_compute TEMP
compute    TEMP all temp
```

### Description
Evaluate the interaction of the system by using [Deep Potential][DP] or [Deep Potential Smooth Edition][DP-SE]. It is noticed that deep potential is not a "pairwise" interaction, but a multi-body interaction.

This pair style takes the deep potential defined in a model file that usually has the .pb extension. The model can be trained and frozen by package mdpu-kit, which can have either double or single float precision interface.

The model deviation evalulates the consistency of the force predictions from multiple models. By default, only the maximal, minimal and average model deviations are output. If the key `atomic` is set, then the model deviation of force prediction of each atom will be output.

By default, the model deviation is output in absolute value. If the keyword `relative` is set, then the relative model deviation of the force will be output, including values output by the keyword `atomic`. The relative model deviation of the force on atom $i$ is defined by

$$E_{f_i}=\frac{\left|D_{f_i}\right|}{\left|f_i\right|+l}$$

where $D_{f_i}$ is the absolute model deviation of the force on atom $i$, $f_i$ is the norm of the force and $l$ is provided as the parameter of the keyword `relative`.
If the keyword `relative_v` is set, then the relative model deviation of the virial will be output instead of the absolute value, with the same definition of that of the force:

$$E_{v_i}=\frac{\left|D_{v_i}\right|}{\left|v_i\right|+l}$$

If the keyword `fparam` is set, the given frame parameter(s) will be fed to the model.
If the keyword `fparam_from_compute` is set, the global parameter(s) from compute command (e.g., temperature from [compute temp command](https://docs.lammps.org/compute_temp.html)) will be fed to the model as the frame parameter(s).
If the keyword `aparam` is set, the given atomic parameter(s) will be fed to the model, where each atom is assumed to have the same atomic parameter(s).
If the keyword `ttm` is set, electronic temperatures from [fix ttm command](https://docs.lammps.org/fix_ttm.html) will be fed to the model as the atomic parameters.

Only a single `pair_coeff` command is used with the mdpu style which specifies atom names. These are mapped to LAMMPS atom types (integers from 1 to Ntypes) by specifying Ntypes additional arguments after `* *` in the `pair_coeff` command.
If atom names are not set in the `pair_coeff` command, the training parameter {ref}`type_map <model/type_map>` will be used by default.
If the training parameter {ref}`type_map <model/type_map>` is not set, atom names in the `pair_coeff` command cannot be set. In this case, atom type indexes in [`type.raw`](../data/system.md) (integers from 0 to Ntypes-1) will map to LAMMPS atom types.

Spin is specified by keywords `virtual_len` and `spin_norm`. If the keyword `virtual_len` is set, the distance between virtual atom and its corresponding real atom for each type of magnetic atoms will be fed to the model as the spin parameters. If the keyword `spin_norm` is set, the magnitude of the magnetic moment for each type of magnetic atoms will be fed to the model as the spin parameters.

