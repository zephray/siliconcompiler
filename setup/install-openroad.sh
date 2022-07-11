#!/bin/sh

# exit when any command fails
set -e

src_path=$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)

sudo apt-get install -y pkg-config build-essential libatomic-ops-dev python3 bison flex libreadline-dev gawk libffi-dev git graphviz tcl xdot libboost-system-dev libboost-python-dev libboost-filesystem-dev libboost-serialization-dev libboost-thread-dev zlib1g-dev cmake swig libeigen3-dev
sudo apt-get install -y libboost-test-dev libspdlog-dev libqt5opengl5-dev

mkdir -p deps
cd deps

wget -q http://lemon.cs.elte.hu/pub/sources/lemon-1.3.1.tar.gz
tar -xf lemon-1.3.1.tar.gz
cd lemon-1.3.1
cmake -B build .
sudo cmake --build build -j $(nproc) --target install
cd -

wget -q https://prdownloads.sourceforge.net/tcl/tcl8.6.10-src.tar.gz
tar -xf tcl8.6.10-src.tar.gz
cd tcl8.6.10/unix
./configure
make
sudo make install
cd -

sudo ln -s /usr/bin/python3 /usr/bin/python
sudo ln -s /usr/local/lib/libtcl8.6.so /usr/local/lib/libtcl.so

cd ${src_path}/..

if git status > /dev/null; then
    # If we're in a Git repo, use the submodule
    git submodule update --init --recursive third_party/tools/openroad
    cd third_party/tools/openroad
else
    # Otherwise, clone into deps/
    git clone https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts.git deps/openroad
    cd deps/openroad
    # TODO: single source of truth between this and submodule
    git checkout 3bdbd4e6
fi

./build_openroad.sh -o

echo "Please add \"source $(pwd)/setup_env.sh\" to your .bashrc"

cd -
