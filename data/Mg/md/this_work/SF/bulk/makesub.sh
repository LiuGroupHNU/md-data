st=`echo "$1 0" | awk '{print $1}'`
ed=`echo "$2 3" | awk '{print $1}'`

for j in $(seq $st 1 $ed);do
mkdir $j; 
cp $j.dat $j/input.dat; 
cp in.lammps $j; 
cd $j; 
ln -s ../model.pb; 
#sbatch slurm.sh; 
mpirun -np 1 lmp_mpi < in.lammps
cd ../; 
sleep 3
done
