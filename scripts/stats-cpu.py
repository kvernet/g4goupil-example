#! /usr/bin/env python3
from alive_progress import alive_bar
import argparse
import os
import numpy
import pickle
import subprocess


def get_stats(path):
    with open(path, "rb") as f:
        d = pickle.load(f)        
    return d["n_generated"], len(d["expected"])


def get_elapsed(jobid):
    r = subprocess.run(f"sacct -j {jobid} --format='JobIDRaw,Elapsed'",
        shell=True, capture_output=True, check=True)
    elapsed = []
    for line in r.stdout.decode().split(os.linesep)[2::2]:
        if not line: continue
        raw, line = line.split()
        raw = int(raw)
        if "-" in line:
            d, hms = line.split("-", 1)
            d = int(d)
        else:
            d = 0
            hms = line
        h, m, s = map(int, hms.split(":"))
        
        elapsed.append((raw, s  + 60 * (m + 60 * (h + 24 * d))))
    return elapsed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute cpu.")
    
    parser.add_argument("-f",
        dest="files",
        help="input files",
        nargs="+")
    
    args = parser.parse_args()

    generated, selected = 0, 0
    jobids = set()
    elapsed = {}
    with alive_bar(len(args.files)) as bar:
        for filename in args.files:
            ng, ns = get_stats(filename)
            generated += ng
            selected += ns
            filename = os.path.basename(filename)
            name, ext = os.path.splitext(filename)
            jobid = int(name.split("-")[1])
            if jobid not in jobids:
                for (raw, el) in get_elapsed(jobid):
                    if raw in elapsed:
                        assert(elapsed[raw] == el)
                    elapsed[raw] = el
                jobids.add(jobid)
            bar()
    total_elapsed = sum(elapsed.values())

    print(f"# of jobs = {len(elapsed)}")
    print(f"generated = {generated}")
    print(f"selected  = {selected}")
    print(f"elapsed   = {total_elapsed} s")
