G4GOUPIl_DIR=$(shell python3 -m goupil --prefix)/interfaces/geant4

CFLAGS= -O2 \
        -Iinclude \
        -I$(G4GOUPIl_DIR) \
        $(shell geant4-config --cflags)
        
LIBS= $(shell geant4-config --libs)

lib/libgeometry.so: src/G4Geometry.cpp include/G4Geometry.hh lib
	$(CXX) $(CFLAGS) -shared -fPIC -o $@ $< $(G4GOUPIl_DIR)/G4Goupil.cc $(LIBS)

lib:
	mkdir -p lib

clean:
	rm -rf lib
