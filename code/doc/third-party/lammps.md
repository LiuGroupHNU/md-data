# Run MD with LAMMPS

Running an MD simulation with LAMMPS is simpler. In the LAMMPS input file, one needs to specify the pair style as follows

```lammps
pair_style     mdpu model.pb
pair_coeff     * *
```
where `model.pb` is the file name of the frozen model. 
