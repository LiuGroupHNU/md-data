set -e

SCRIPT_PATH=$(dirname $(realpath -s $0))
if [ -z "$INSTALL_PREFIX" ]; then
	INSTALL_PREFIX=$(realpath -s ${SCRIPT_PATH}/../../dp)
fi
mkdir -p ${INSTALL_PREFIX}
echo "Installing mdpu-kit to ${INSTALL_PREFIX}"
NPROC=$(nproc --all)

#------------------

BUILD_TMP_DIR=${SCRIPT_PATH}/../build
mkdir -p ${BUILD_TMP_DIR}
cd ${BUILD_TMP_DIR}
cmake -DCMAKE_INSTALL_PREFIX=${INSTALL_PREFIX} -DMDPU_C_ROOT=${MDPU_C_ROOT} -DLAMMPS_VERSION=stable_23Jun2022_update4 ..
make -j${NPROC}
make install
make lammps

#------------------
echo "Congratulations! mdpu-kit has been installed at ${INSTALL_PREFIX}"
