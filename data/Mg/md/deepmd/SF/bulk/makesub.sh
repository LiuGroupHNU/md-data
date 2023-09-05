for j in {0..3};do 
mkdir $j; 
cp $j.dat $j/input.dat; 
cp in.lammps $j; 
cd $j; 
ln -s ../model.pb; 
#sbatch slurm.sh; 
mpirun -np 1 lmp_mpi < in.lammps
cd ../; 
done
