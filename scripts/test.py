#! /usr/bin/env python3
import ctypes
import goupil
import pickle

# Lib path
lib_path = "lib/libgeometry.so"

# Load shared library.
clib = ctypes.CDLL(lib_path)

# Load geometry
geometry = goupil.ExternalGeometry(lib_path)

# Define & configure the engine transport
engine = goupil.TransportEngine(geometry)
engine.boundary = 2 # Termination when sector with index 2 is entered. 

states = goupil.states(10000000)

# Prototype library functions.
clib.g4randomize_states.argtypes = [ctypes.c_size_t, ctypes.c_void_p]
clib.g4randomize_states.restype = None

clib.g4randomize_states(states.size, states.ctypes.data)

primaries = states.copy()
status = engine.transport(states)

from goupil_analysis import DataSummary
sel0 = (status == goupil.TransportStatus.BOUNDARY) & (states["energy"] < primaries["energy"])
sel1 = (status == goupil.TransportStatus.BOUNDARY) & (states["energy"] == primaries["energy"])

data = {}
for i, sel in enumerate((sel0, sel1)):
    s, p = states[sel], primaries[sel]
    energies = s["energy"]
    cos_theta = numpy.sum(s["direction"] * p["direction"], axis=1)
    distances = numpy.linalg.norm(s["position"] - p["position"], axis=1)
    tag = "continuous" if i == 0 else "discrete"
    data[tag] = DataSummary.new(states.size, energies, cos_theta, distances)

with open("goupil.forward.pkl", "wb") as f:
    pickle.dump(data, f)
