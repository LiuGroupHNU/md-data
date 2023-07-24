PYTHON=/home/pc2/InstallPackage/Application/Anaconda/bin/python
MPIRUN=/home/pc2/InstallPackage/Application/mpich/install/bin/mpirun
LMP=/home/pc2/InstallPackage/Application/lammps/lammps-4May2022/src/lmp_mpi

sudo $MPIRUN -np 1 $LMP < input.lammps 

