#ifndef g4geometry_h
#define g4geometry_h

/* Geant4 interface */
#include "G4VUserDetectorConstruction.hh"
/* Goupil interface */
#include "goupil.h"

#include <array>

/*TODO Define in goupil.h */
struct goupil_state {
    goupil_float_t energy;
    struct goupil_float3 position;
    struct goupil_float3 direction;
    goupil_float_t length;
    goupil_float_t weight;
};

struct DetectorConstruction : public G4VUserDetectorConstruction {
    public:
        static DetectorConstruction * Singleton();
        G4VPhysicalVolume * Construct();
        
        void RandomiseState(struct goupil_state * state);
        double RandomiseBackward(struct goupil_state * state);
        
        G4double worldSize[3], detectorSize[3];
        G4double airSize[3], groundSize[3];
        G4double detectorOffset;
    
    private:
        DetectorConstruction();
        ~DetectorConstruction() override = default;
        
        std::array<std::pair<double, double>, 11> spectrum = {
            // Po^218 -> Pb^214.
            std::make_pair(0.242,  7.3),
            std::make_pair(0.295, 18.4),
            std::make_pair(0.352, 35.6),
            // Pb^214 -> Bi^214.
            std::make_pair(0.609, 45.5),
            std::make_pair(0.768,  4.9),
            std::make_pair(0.934,  3.1),
            std::make_pair(1.120, 14.9),
            std::make_pair(1.238,  5.8),
            std::make_pair(1.378,  4.0),
            std::make_pair(1.764, 15.3),
            std::make_pair(2.204,  4.9),
        };
};

#endif
