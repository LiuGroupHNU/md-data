
now_dir=`pwd`

for t in $@
do
ws=${t}-expand

echo $ws
cd $ws

for ii in $(seq 0 1 2)
do

cd $ii
pwd

cp ../../input.lammps .
cp ../../model.pb .

seed=$((ii+1))

sed -i "s#%temp%#${t}#g" input.lammps
sed -i "s#%seed%#${seed}#g" input.lammps

bash ../../run.sh


cd ..
chmod +777 -R --silent $ii
done
cd ..
chmod +777 -R --silent $ws
done

