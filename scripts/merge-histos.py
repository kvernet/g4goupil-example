#!/usr/bin/env python3
import argparse
import numpy
import pickle

from goupil_analysis import DataSummary, Histogramed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge histograms.")
    
    parser.add_argument("files",
        help="input files",
        nargs="+")

    args = parser.parse_args()

    forward = args.files[0].endswith(".forward.pkl")

    all_data = []
    for file in args.files:
        print(f"processing {file}")
        with open(file, "rb") as f:
            d = pickle.load(f)
        all_data.append(d)

    continuous = DataSummary.sum([d["continuous"] for d in all_data])
    discrete = DataSummary.sum([d["discrete"] for d in all_data])
    if forward:
        data = {
            "continuous": continuous,
            "discrete": discrete,
        }
    else:
        energy_thin = Histogramed.sum([d["energy_thin"] for d in all_data])
        data = {
            "continuous": continuous,
            "discrete": discrete,
            "energy_thin": energy_thin,
        }

    tag = "forward" if forward else "backward"
    with open(f"goupil.{tag}.pkl", "wb") as f:
        pickle.dump(data, f)
