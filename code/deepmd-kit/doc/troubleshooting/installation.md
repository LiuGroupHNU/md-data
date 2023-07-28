# Installation
## Inadequate versions of gcc/g++
Sometimes you may use a gcc/g++ of version < 4.8. Or if you have a gcc/g++ of version > 4.8, say, 7.2.0, you may choose to use it by doing
```bash
export CC=/path/to/gcc-7.2.0/bin/gcc
export CXX=/path/to/gcc-7.2.0/bin/g++
```

## Build files left in DeePMD-kit
When you try to build a second time when installing DeePMD-kit, files produced before may contribute to failure. Thus, you may clear them by
```bash
cd build
rm -r *
```
and redo the `cmake` process.
