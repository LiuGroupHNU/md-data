

# Usage

the result of this_work

# dataset

| Material | Dataset Reference | Sample Method |
| -- | -- | -- |
| Au | 10.48550/arXiv.2006.13136 | DP-GEN |
| Cu | 10.1016/j.cpc.2020.107206 | DP-GEN |
| Mg | 10.1103/PhysRevMaterials.3.023804 | DP-GEN |
| GeTe | 10.1109/LED.2020.2964779 | AIMD |
| H2O | 10.1016/j.cpc.2020.107206, 10.1103/PhysRevLett.126.236001 | DP-GEN |
| LiGePS | 10.1063/5.0041849 | DP-GEN |

# md

`lmp_mpi` represents the parallel version of LAMMPS software.


## Au

running MD:

``` bash
cd ws
lmp_mpi < in.equil
```

post-prcessing:

``` bash
python main.py
```

## Cu

running MD:

``` bash
cd 1 # or 2,3,4,5
lmp_mpi < in.lmp
```

post-processing:

``` bash
python main.py
```

## GeTe

running MD:

``` bash
cd this_work
lmp_mpi < in.lmp
```

You can get the trajectory file of amorphous GeTe.
And use ovito extract RDF, ADF, CN, and ALTBC.
The results is generated in amorphous/this_work folder.

post-processing:

``` bash
python main.py
```

## H2O

running MD:

``` bash
cd ws1 # or ws2,ws3,ws4,ws5
lmp_mpi < water_rdf.in
```

post-processing:

``` bash
python main.py
```

## LiGePS

running MD:

``` bash
cd this_work
cd 300-expand # or 400-expand, 500-expand, 666-expand, 800-expand, and 1000-expand
lmp_mpi < input.lammps
```

post-processing:

``` bash
python main.py
```

## Mg

running MD:

``` bash
# bulk
cd this_work/SF
cd bulk
cp $model model.pb
bash makesub.sh
tar -cvf min.tar */min.dat
cp min.tar ../SF
# SF
cd ../SF
tar -xvf min.tar
cp $model model.pb
bash makeSF.sh
bash sub.sh
bash postsf.sh
cd ../plot
cp ../SF/*txt .
```

post-processing:

``` bash
python main.py
```
