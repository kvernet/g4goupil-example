#!/usr/bin/env python3
import argparse
import numpy
import pickle

from goupil_analysis import DataSummary, Histogramed

def getData(paths):
    events = 0
    primaries = []
    expected = []
    for path in paths:
        with open(path, "rb") as f:
            d = pickle.load(f)
        
        primaries.append(d["primaries"])
        expected.append(d["expected"])
        events += d["n_generated"]
        
    def unpack(a):
        n = sum(ai.size for ai in a)
        b = numpy.empty(n, dtype=a[0].dtype)
        i = 0
        for ai in a:
            m = ai.size
            b[i:i+m] = ai
            i += m
        return b
    
    primaries = unpack(primaries)
    expected = unpack(expected)
    
    return {
        "n_generated": events,
        "expected": expected,
        "primaries": primaries
    }
    
def process_data(files, forward):

    data = getData(files)
    
    sel0 = data["expected"]["energy"] < data["primaries"]["energy"]
    sel1 = data["expected"]["energy"] == data["primaries"]["energy"]
      
    def histograms(sel, discrete=False):
        energies = data["expected"]["energy"][sel]
        cos_theta = numpy.sum(data["expected"]["direction"][sel] * data["primaries"]["direction"][sel], axis=1)
        distances = numpy.linalg.norm(
            data["expected"]["position"][sel] - data["primaries"]["position"][sel],
            axis = 1
        )
        weights = None if forward else data["expected"]["weight"][sel]
        return DataSummary.new(
            data["n_generated"],
            energies,
            cos_theta,
            distances,
            discrete=discrete,
            weights=weights
        )
        
    continuous = histograms(sel0)
    discrete = histograms(sel1, discrete=True)
    
    if not forward:
        expected = data["expected"][sel0]
        energy_thin = Histogramed.energy_thin(
            data["n_generated"],
            expected["energy"],
            weights = expected["weight"]
        )
    
    # Export results.
    data = {
        "continuous": continuous,
        "discrete": discrete,
    }
    
    if not forward:
        data["energy_thin"] = energy_thin    
        
    return data
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot simulation data.")
    
    parser.add_argument("-f",
        dest="files",
        help="input files",
        nargs="+")
    
    args = parser.parse_args()
    
    forward = args.files[0].endswith(".forward.pkl")

    if forward:
        data = process_data(args.files, True)
    else:
        all_data = []
        for file in args.files:
            print(f"processing {file}")
            d = process_data((file,), False)
            all_data.append(d)
        continuous = DataSummary.sum([d["continuous"] for d in all_data])
        discrete = DataSummary.sum([d["discrete"] for d in all_data])
        energy_thin = Histogramed.sum([d["energy_thin"] for d in all_data])
        
        data = {
            "continuous": continuous,
            "discrete": discrete,
            "energy_thin": energy_thin,
        }
    
    tag = "forward" if forward else "backward"
    with open(f"goupil.{tag}.pkl", "wb") as f:
        pickle.dump(data, f)
