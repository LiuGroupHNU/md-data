


temp=$1
if [ "" = "$temp" ]
then
echo "Please input temp"
exit
fi

now_dir=`pwd`
echo $now_dir
for ((ii=1; ii<4; ii++))
do
ws=$temp/$ii
echo $ws
mkdir -p $ws
cd $ws

# LiGePS-SSE-PBE-model.pb is model.pb
# LiGePS-SSE-PBEsol-model.pb is model2.pb 
cp $now_dir/inputs/model2.pb ./model.pb
cp $now_dir/inputs/input.lammps ./input.lammps
cp $now_dir/inputs/lmp.sub ./lmp.sub
sed -i "s#%temp%#$temp#g" input.lammps
sed -i "s#%seed%#$ii#g" input.lammps
# lmp < input.lammps
sbatch lmp.sub

rm -r model.pb
cd $now_dir
done



