# Import necessary libraries
import pyg4ometry as pg4
import numpy as np
from legendhpges import make_hpge
from pygeomtools.viewer import visualize
from pygeomtools.write import write_pygeom
from pygeomtools.detectors import generate_detector_macro, RemageDetectorInfo

# Step 1: Create a Geant4 registry
reg = pg4.geant4.Registry()

# Step 2: Define the world volume
world_solid = pg4.geant4.solid.Box("world_solid", 500, 500, 500, reg, "mm")
world_logical = pg4.geant4.LogicalVolume(world_solid, "G4_Galactic", "world_logical", reg)
reg.setWorld(world_logical.name)

# Step 3: Define the HPGe detector metadata
dummy_metadata = {
    "name": "teststand_hpge",
    "geometry": {
        "height_in_mm": 30,
        "radius_in_mm": 30,
        "groove": {"depth_in_mm": 2.0, "radius_in_mm": {"outer": 10.5, "inner": 7.5}},
        "pp_contact": {"radius_in_mm": 7.5, "depth_in_mm": 0},
        "taper": {
            "top": {"angle_in_deg": 0.0, "height_in_mm": 0.0},
            "bottom": {"angle_in_deg": 0.0, "height_in_mm": 0.0},
        },
    },
    "production": {"enrichment": 0.0775},
    "type": "bege",
}

# Step 4: Create the HPGe detector
hpge = make_hpge(dummy_metadata, name="hpge_logical", registry=reg)
z_height_hpge = dummy_metadata["geometry"]["height_in_mm"]

# Step 5: Place the HPGe detector in the world volume
det_pv = pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0, "mm"], hpge, "hpge_physical", world_logical, registry=reg)

# Step 6: Register the HPGe detector as sensitive volume with "germanium" output scheme and rawid 001
det_pv.set_pygeom_active_detector(RemageDetectorInfo("germanium", "001", dummy_metadata))

# Step 7: Define the vacuum gap and aluminum holder
radius = 35
height = 100
vacuum_gap = 5
al_width = 1


# Step 9: Create the aluminum holder parts
al_part_1 = pg4.geant4.solid.Tubs(
    "al_part_1", 0, radius, al_width, 0, 2 * np.pi, reg, "mm"
)
al_part_2 = pg4.geant4.solid.Tubs(
    "al_part_2",
    radius - al_width,
    radius,
    (vacuum_gap + height),
    0,
    2 * np.pi,
    reg,
    "mm",
)
al_solid = pg4.geant4.solid.Union(
    "al_solid",
    al_part_1,
    al_part_2,
    [[0, 0, 0], [0, 0, -height/2. - al_width, "mm"]],
    reg,
)
al_logical = pg4.geant4.LogicalVolume(al_solid, "G4_Al", "al_logical", reg)

# Step 10: Place the aluminum holder in the world volume
pg4.geant4.PhysicalVolume(
    [0, 0, 0],
    [0, 0, z_height_hpge+ vacuum_gap, "mm"],
    al_logical,
    "al_p",
    world_logical,
    registry=reg,
)
al_logical.pygeom_color_rgba = [0.5, 0.5, 0.5, 0.5]

# Step 11: Define the source holder
src_holder_thickness = 2
src_holder_solid = pg4.geant4.solid.Box(
    "src_holder_solid", 20, 10, src_holder_thickness, reg, "mm"
)
src_holder_logical = pg4.geant4.LogicalVolume(
    src_holder_solid, "G4_GLASS_PLATE", "src_holder_logical", reg
)

# Step 12: Place the source holder in the world volume
pg4.geant4.PhysicalVolume(
    [0, 0, 0],
    [0, 0,  z_height_hpge + vacuum_gap + al_width + src_holder_thickness / 2.0, "mm"],
    src_holder_logical,
    "src_holder_p",
    world_logical,
    registry=reg,
)
src_holder_logical.pygeom_color_rgba = [1, 1, 1, 0.25]

# Step 13: Define the source
src_solid = pg4.geant4.solid.Box("src_solid", 1, 1, 1, reg, "mm")
src_logical = pg4.geant4.LogicalVolume(src_solid, "G4_GLASS_PLATE", "src_logical", reg)

# Step 14: Place the source in the source holder
pg4.geant4.PhysicalVolume(
    [0, 0, 0], [0, 0, 0, "mm"], src_logical, "src_physical", src_holder_logical, registry=reg
)
src_logical.pygeom_color_rgba = [1, 0, 0, 0.25]

# Step 15: Visualize the geometry
visualize(reg)

# Step 16: Write out macro commands to register the sensitive volumes to remage
generate_detector_macro(reg, "pv_reg.mac")

# Step 17: Write the geometry to a GDML file
write_pygeom(reg, "simple_teststand.gdml")


