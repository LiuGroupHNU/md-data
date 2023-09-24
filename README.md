# Usage
This is open-sourced code and data for paper entitiled "Breaking the Speed, Power, Cost and Size Limits of Molecular Dynamics with Ab Initio Accuracy".

# code
The `code` folder, which contains the generation that implements mdpu (Molecular Dynamics Processing Unit) training. You can install and use the code according to the [documentation](code/README.md).

# data
For each material, two folders (`train` and `md`) are kept in its corresponding directory.

The `train` contains the input scripts and results of the training. The training step is divided into 2 steps to train CNN and QNN. You can type `dp train-mdpu train_cnn.json -s s1` to train CNN and get the corresponding `mdpu_cnn` folder. You can type `dp train-mdpu train_qnn.json -s s2` to train QNN and get the corresponding `mdpu_qnn` folder. The file `mdpu_qnn/model.pb` is the model file used to perform the mdpu MD.

The `md` contains the input scripts for the mdpu MD, the model files, the output files, and the post-processing files for the results. You can run mdpu MD by uploading input scripts and model files to an online server and running MD through the [Bohrium](https://bohrium.dp.tech).

For more details about `train` and `md`, please refer to the [documentation](code/doc/mdpu/index.md).
