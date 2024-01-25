#! /usr/bin/env python3
import ctypes
import goupil

# Lib path
lib_path = "lib/libgeometry.so"

# Load shared library.
clib = ctypes.CDLL(lib_path)

# Load geometry
geometry = goupil.ExternalGeometry(lib_path)

# Define & configure the engine transport
engine = goupil.TransportEngine(geometry)
engine.mode = "Backward"

states = goupil.states(20, energy=0.5)
states["energy"] = 0

# Prototype library functions.
clib.g4randomize_states.argtypes = [ctypes.c_size_t,
    ctypes.c_void_p, ctypes.c_bool]
clib.g4randomize_states.restype = None

clib.g4randomize_states(states.size, states.ctypes.data, False)
print(states["energy"])

constraints = max(states["energy"])

status = engine.transport(states, constraints=constraints)
print(status)
