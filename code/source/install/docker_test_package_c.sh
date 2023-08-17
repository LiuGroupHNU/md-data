# test libmdpu_c.tar.gz works with gcc 4.9.0, glibc 2.19
set -e

SCRIPT_PATH=$(dirname $(realpath -s $0))

# assume libmdpu_c.tar.gz has been created

wget "https://drive.google.com/uc?export=download&id=1xldLhzm4uSkq6iPohSycNWAsWqKAenKX" -O ${SCRIPT_PATH}/../../examples/infer_water/"graph.pb"

docker run --rm -v ${SCRIPT_PATH}/../..:/root/mdpu-kit -w /root/mdpu-kit \
	gcc:4.9 \
	/bin/sh -c "tar vxzf libmdpu_c.tar.gz \
            && cd examples/infer_water \
            && gcc infer_water.c -std=c99 -L ../../libmdpu_c/lib -I ../../libmdpu_c/include -Wl,--no-as-needed -lmdpu_c -Wl,-rpath=../../libmdpu_c/lib -o infer_water \
            && ./infer_water"
