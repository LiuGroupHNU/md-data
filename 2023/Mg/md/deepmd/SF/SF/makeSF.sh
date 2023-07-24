now_dir=`pwd`
rep_py=$now_dir/../run_replace.py

cd 0
a=`python $rep_py min.dat 7 2`
b=`python $rep_py min.dat 9 3`
for j in $(seq 0 0.025 1);do 
    mkdir $j
    cp min.dat $j/input.dat
    cd $j
    c=`echo "$a*$j"|bc`
    ls
    python $rep_py input.dat 9 3 $c 
    cd ../
    echo "$j $a $b $c"
done
cd ../1
a=`python $rep_py min.dat 6 2`
b=`python $rep_py min.dat 9 1`
for j in $(seq 0 0.025 1);do
    mkdir $j
    cp min.dat $j/input.dat
    cd $j
    c=`echo "1.0*$a*$j*0.5"|bc`
    python $rep_py input.dat 9 1 $c 
    cd ../
done
cd ../2
a=`python $rep_py min.dat 6 2`
b=`python $rep_py min.dat 9 2`
for j in $(seq 0 0.025 1);do
    mkdir $j
    cp min.dat $j/input.dat
    cd $j
    c=`echo "1.0*$b-$a*$j"|bc`
    python $rep_py input.dat 9 2 $c 
    cd ../
done
cd ../3
a=`python $rep_py min.dat 6 2`
b=`python $rep_py min.dat 9 2`
for j in $(seq 0 0.025 1);do
    mkdir $j
    cp min.dat $j/input.dat
    cd $j
    c=`echo "1.0*$b-$a*$j*0.5"|bc`
    python $rep_py input.dat 9 2 $c 
    echo "# j $j a $a b $b c $c"
    cd ../
done
cd ../