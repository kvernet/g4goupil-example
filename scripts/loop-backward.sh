#! /bin/bash

mkdir -p data
for i in $(seq 1 100); do
    echo "processesing ${i} / 100"
    ./scripts/test-backward.py
    mv goupil.backward.pkl data/goupil.backward.${i}.pkl
done
