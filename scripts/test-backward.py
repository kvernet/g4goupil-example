#! /usr/bin/env python3
import ctypes
import goupil
import numpy
import pickle

# Lib path
lib_path = "lib/libgeometry.so"

# Load shared library.
clib = ctypes.CDLL(lib_path)

# Load geometry
geometry = goupil.ExternalGeometry(lib_path)

# Define & configure the engine transport
engine = goupil.TransportEngine(geometry)
engine.mode = "Backward"
engine.boundary = 2 # Termination when sector with index 2 is entered. 

states = goupil.states(10000000)
sources_energies = numpy.empty(states.size)

# Prototype library functions.
clib.g4randomize_backward.argtypes = [ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p]
clib.g4randomize_backward.restype = None

clib.g4randomize_source_volume.argtypes = []
clib.g4randomize_source_volume.restype = ctypes.c_double

clib.g4randomize_backward(states.size, states.ctypes.data, sources_energies.ctypes.data)

expected = states.copy()
status = engine.transport(states, sources_energies)

from goupil_analysis import DataSummary

expected["weight"] = states["weight"]
primaries = states
states = expected

sectors = geometry.locate(primaries)
valid = (status == goupil.TransportStatus.ENERGY_CONSTRAINT) & (sectors == 1)
states["weight"][valid] /= clib.g4randomize_source_volume() * 4.0 * numpy.pi

sel0 = valid & (states["energy"] < primaries["energy"])
sel1 = valid & (states["energy"] == primaries["energy"])

data = {}
for i, sel in enumerate((sel0, sel1)):
    s, p = states[sel], primaries[sel]
    energies = s["energy"]
    cos_theta = numpy.sum(s["direction"] * p["direction"], axis=1)
    distances = numpy.linalg.norm(s["position"] - p["position"], axis=1)
    tag = "continuous" if i == 0 else "discrete"
    data[tag] = DataSummary.new(states.size, energies, cos_theta, distances, s["weight"])

with open("goupil.backward.pkl", "wb") as f:
    pickle.dump(data, f)
