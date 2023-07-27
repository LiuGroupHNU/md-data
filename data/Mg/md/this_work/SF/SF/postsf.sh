cd 0
pwd
a1=`awk 'NR==6{print $1}' min.dat`
a2=`awk 'NR==6{print $2}' min.dat`
b1=`awk 'NR==7{print $1}' min.dat`
b2=`awk 'NR==7{print $2}' min.dat`
# A=`echo "(($a2)-($a1))*(($b2)-($b1))"|bc`
A=`echo "$a1 $a2 $b1 $b2" | awk '{printf("%f",($2-$1)*($4-$3))}'`
cd 0.000
N=`grep "Total number of atoms" log.lammps|tail -n1|awk '{print $6}' `
E=`grep "Final energy per atoms" log.lammps|tail -n1|awk '{print $6}' `
E1=`echo "$N*$E"|bc`
cd ../
for j in $(seq 0.000 0.025 1.000);do 
    cd $j
    pwd
    N=`grep "Total number of atoms" log.lammps|tail -n1|awk '{print $6}' `
    E=`grep "Final energy per atoms" log.lammps|tail -n1|awk '{print $6}' `
    E2=`echo "$N*$E"|bc`
    X=`echo "scale=5;16000.00*(($E2)-($E1))/$A"|bc`
    echo $X >> ../../basal.txt
    cd ../
done
cd ../1
pwd
a1=`awk 'NR==6{print $1}' min.dat`
a2=`awk 'NR==6{print $2}' min.dat`
b1=`awk 'NR==8{print $1}' min.dat`
b2=`awk 'NR==8{print $2}' min.dat`
# A=`echo "(($a2)-($a1))*(($b2)-($b1))"|bc`
A=`echo "$a1 $a2 $b1 $b2" | awk '{printf("%f",($2-$1)*($4-$3))}'`
cd 0.000
N=`grep "Total number of atoms" log.lammps|tail -n1|awk '{print $6}' `
E=`grep "Final energy per atoms" log.lammps|tail -n1|awk '{print $6}' `
E1=`echo "$N*$E"|bc`
cd ../
for j in $(seq 0.000 0.025 1.000);do 
    cd $j
    pwd
    N=`grep "Total number of atoms" log.lammps|tail -n1|awk '{print $6}' `
    E=`grep "Final energy per atoms" log.lammps|tail -n1|awk '{print $6}' `
    E2=`echo "$N*$E"|bc`
    X=`echo "scale=5;16000.00*(($E2)-($E1))/$A"|bc`
    echo $X >> ../../prismatic.txt
    cd ../
done
cd ../2
pwd
a1=`awk 'NR==6{print $1}' min.dat`
a2=`awk 'NR==6{print $2}' min.dat`
b1=`awk 'NR==7{print $1}' min.dat`
b2=`awk 'NR==7{print $2}' min.dat`
# A=`echo "(($a2)-($a1))*(($b2)-($b1))"|bc`
A=`echo "$a1 $a2 $b1 $b2" | awk '{printf("%f",($2-$1)*($4-$3))}'`
cd 0.000
N=`grep "Total number of atoms" log.lammps|tail -n1|awk '{print $6}' `
E=`grep "Final energy per atoms" log.lammps|tail -n1|awk '{print $6}' `
E1=`echo "$N*$E"|bc`
cd ../
for j in $(seq 0.000 0.025 1.000);do 
    cd $j
    pwd
    N=`grep "Total number of atoms" log.lammps|tail -n1|awk '{print $6}' `
    E=`grep "Final energy per atoms" log.lammps|tail -n1|awk '{print $6}' `
    E2=`echo "$N*$E"|bc`
    X=`echo "scale=5;16000.00*(($E2)-($E1))/$A"|bc`
    echo $X >> ../../pyramidalI.txt
    cd ../
done
cd ../3
pwd
a1=`awk 'NR==6{print $1}' min.dat`
a2=`awk 'NR==6{print $2}' min.dat`
b1=`awk 'NR==7{print $1}' min.dat`
b2=`awk 'NR==7{print $2}' min.dat`
# A=`echo "(($a2)-($a1))*(($b2)-($b1))"|bc`
A=`echo "$a1 $a2 $b1 $b2" | awk '{printf("%f",($2-$1)*($4-$3))}'`
cd 0.000
N=`grep "Total number of atoms" log.lammps|tail -n1|awk '{print $6}' `
E=`grep "Final energy per atoms" log.lammps|tail -n1|awk '{print $6}' `
E1=`echo "$N*$E"|bc`
cd ../
for j in $(seq 0.000 0.025 1.000);do 
    cd $j
    pwd
    N=`grep "Total number of atoms" log.lammps|tail -n1|awk '{print $6}' `
    E=`grep "Final energy per atoms" log.lammps|tail -n1|awk '{print $6}' `
    E2=`echo "$N*$E"|bc`
    X=`echo "scale=5;16000.00*(($E2)-($E1))/$A"|bc`
    echo $X >> ../../pyramidalII.txt
    cd ../
done
cd ../

