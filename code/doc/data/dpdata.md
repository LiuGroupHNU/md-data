# Prepare data with dpdata

One can use a convenient tool [`dpdata`](https://github.com/deepmodeling/dpdata) to convert data directly from the output of first principle packages to the mdpu-kit format.

To install one can execute
```bash
pip install dpdata
```

An example of converting data [VASP](https://www.vasp.at/) data in `OUTCAR` format to mdpu-kit data can be found at
```
$mdpu_source_dir/examples/data_conv
```

Switch to that directory, then one can convert data by using the following python script
```python
import dpdata

dsys = dpdata.LabeledSystem("OUTCAR")
dsys.to("deepmd/npy", "mdpu_data", set_size=dsys.get_nframes())
```

`get_nframes()` method gets the number of frames in the `OUTCAR`, and the argument `set_size` enforces that the set size is equal to the number of frames in the system, viz. only one `set` is created in the `system`.

The data in mdpu-kit format is stored in the folder `mdpu_data`.

A list of all [supported data format](https://github.com/deepmodeling/dpdata#load-data) and more nice features of `dpdata` can be found on the [official website](https://github.com/deepmodeling/dpdata).
