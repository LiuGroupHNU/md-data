
# nvnmd_cnn64
cd nvnmd_cnn
python ../../run_freeze_mapt.py

cd ../
mkdir nvnmd_cnn64
cd nvnmd_cnn64
cp ../nvnmd_cnn/train.json .
# edit decay_steps, stop_batch, disp_freq, save_freq, 
#   disp_file, save_ckpt, systems, precision
gedit train.json
python ../../run_freeze_mapt.py
dp transfer -r frozen_model.pb -O ../nvnmd_cnn/frozen_model.pb -o model.pb

model_dir=$1
cp $model_dir model.pb
# bulk
cd bulk
rm -r 0 1 2 3
cp ../model.pb model.pb
sed -i "s/nvnmd/deepmd/g" in.lammps
bash makesub.sh
tar -cvf min.tar */min.dat
cp min.tar ../SF
# SF
cd ../SF
rm -r 0 1 2 3
rm -r *.txt
tar -xvf min.tar
cp ../model.pb model.pb
sed -i "s/nvnmd/deepmd/g" in.lammps.0
sed -i "s/nvnmd/deepmd/g" in.lammps.1
sed -i "s/nvnmd/deepmd/g" in.lammps.2
sed -i "s/nvnmd/deepmd/g" in.lammps.3
bash makeSF.sh
bash sub.sh
bash postsf.sh
cd ../plot
rm -r basal.txt prismatic.txt pyramidalI.txt pyramidalII.txt SF-bench.jpg
cp ../SF/*txt .
python plot-1.py

# bulk
cd bulk
rm -r 0 1 2 3
cp ../model.pb model.pb
sed -i "s/deepmd/nvnmd/g" in.lammps
sudo bash makesub.sh
tar -cvf min.tar */min.dat
cp min.tar ../SF
# SF
cd ../SF
rm -r 0 1 2 3
rm -r *.txt
tar -xvf min.tar
cp ../model.pb model.pb
sed -i "s/deepmd/nvnmd/g" in.lammps.0
sed -i "s/deepmd/nvnmd/g" in.lammps.1
sed -i "s/deepmd/nvnmd/g" in.lammps.2
sed -i "s/deepmd/nvnmd/g" in.lammps.3
bash makeSF.sh
sudo bash sub.sh
bash postsf.sh
cd ../plot
rm -r basal.txt prismatic.txt pyramidalI.txt pyramidalII.txt SF-bench.jpg
cp ../SF/*txt .
python plot-1.py

