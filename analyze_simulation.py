from lgdo import lh5
import pyg4ometry as pg4
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np
from pygeomtools.viewer import visualize

lh5_file = "output.lh5"
sim_data = lh5.read("stp/", lh5_file)

r = pg4.gdml.Reader("simple_teststand.gdml")
reg = r.getRegistry()

det_data = sim_data["det001"].view_as("ak")

evtids = np.unique(det_data["evtid"])
sum_energy = np.array([np.sum(det_data["edep"][det_data["evtid"] == evtid]) for evtid in evtids])

plt.hist(sum_energy, bins=np.linspace(0,3000,301), weights = np.full(len(sum_energy),1/10.))
plt.xlabel(r"E$_\mathrm{dep}$ [keV]")
plt.ylabel("cts / keV")
plt.xlim(0,3000)
plt.show()

scene = {
    "fine_mesh": True,
    "default": {
            "focus": [0, 0, 0],
            "up": [1, 0, 0],
            "camera": [0, 0, 300]
    },
    "scenes": [
        {
            "focus": [0, 0, 0],
            "up": [0, 0, 1],
            "camera": [-300, 0, 0]
        },
    ],
    "points": [
    {
      "file": "output.lh5",
      "table": "stp/vertices",
      "columns": ["xloc", "yloc", "zloc"],
      "color": [0, 1, 0, 1]
    },
    {
      "file": "output.lh5",
      "table": "stp/det001",
      "columns": ["xloc", "yloc", "zloc"],
      "color": [0, 0, 1, 1] 
    }
    ]
}

visualize(reg, scene)

