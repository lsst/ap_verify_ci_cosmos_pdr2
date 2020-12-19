# Config override for lsst.pipe.tasks.calibrate.CalibrateTask
import os.path

from lsst.utils import getPackageDir
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

hscDir = os.path.join(getPackageDir("obs_subaru"), "config")

# Use gaia for astrometry (phot_g_mean for everything, as that is the broadest
# band with the most depth)
# Use panstarrs for photometry (grizy filters)
for refObjLoader in (config.astromRefObjLoader,
                     config.photoRefObjLoader,):
    refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
    # HSC has *lots* of filters, easier to modify the official config
    refObjLoader.load(os.path.join(hscDir, "filterMap.py"))
    # Official config doesn't bother mapping ugrizy names, which are used in Gen 2
    for hscFilter in ["u", "g", "r", "i", "z", "y"]:
        config.astromRefObjLoader.filterMap[hscFilter] = hscFilter

config.connections.astromRefCat = "gaia"
config.astromRefObjLoader.ref_dataset_name = config.connections.astromRefCat
for hscFilter in config.astromRefObjLoader.filterMap:
    config.astromRefObjLoader.filterMap[hscFilter] = "phot_g_mean"

config.connections.photoRefCat = "panstarrs"
config.photoRefObjLoader.ref_dataset_name = config.connections.photoRefCat
