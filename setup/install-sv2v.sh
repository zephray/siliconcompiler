#!/bin/sh

# exit when any command fails
set -e

mkdir -p deps
cd deps

curl -sSL https://get.haskellstack.org/ | sh

git clone https://github.com/zachjs/sv2v.git
cd sv2v
git fetch --tags
git checkout v0.0.9
make
cd ../../
