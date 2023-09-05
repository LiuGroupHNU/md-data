st=`echo "$1 0" | awk '{print $1}'`
ed=`echo "$2 3" | awk '{print $1}'`
st2=`echo "$3 0.000" | awk '{print $1}'`
ed2=`echo "$4 1.000" | awk '{print $1}'`

for k in $(seq $st 1 $ed);do
cp in.lammps.$k $k/in.lammps
cd $k
ln -s ../model.pb
ct=0
for j in $(seq $st2 0.025 $ed2);do 
    cp in.lammps $j; 
    cd $j
    pwd
    ln -s ../model.pb
    #sbatch slurm.sh
    mpirun -np 1 lmp_mpi < in.lammps
    cd ../
    sleep 2 # for high CPU temperature
done
sleep 3
cd ../
done


