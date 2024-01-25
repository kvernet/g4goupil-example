GOUPILDIR= $(shell python3 -m goupil --prefix)/interfaces

CFLAGS= -O0 -g -Isrc/include $(shell geant4-config --cflags)

LIBS= $(shell geant4-config --libs)

SRCS= src/src/G4Geometry.cpp \
    src/src/G4Goupil.cc

lib/libgeometry.so: g4goupil lib
	$(CXX) $(CFLAGS) -shared -fPIC -o $@ $(SRCS) $(LIBS)

g4goupil:
	@ln -fs $(GOUPILDIR)/geant4/G4Goupil.cc $(CURDIR)/src/src/G4Goupil.cc
	@ln -fs $(GOUPILDIR)/geant4/G4Goupil.hh $(CURDIR)/src/include/G4Goupil.hh
	@ln -fs $(GOUPILDIR)/geant4/goupil.h $(CURDIR)/src/include/goupil.h

lib:
	mkdir -p lib

clean:
	rm -rf lib
	rm -f src/src/G4Goupil.cc
	rm -f src/include/G4Goupil.hh
	rm -f src/include/goupil.h
