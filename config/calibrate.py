# Config override for lsst.pipe.tasks.calibrate.CalibrateTask
import os.path

from lsst.utils import getPackageDir

hscDir = os.path.join(getPackageDir("obs_subaru"), "config")

# Use gaia for astrometry (phot_g_mean for everything, as that is the broadest
# band with the most depth).
config.connections.astromRefCat = "gaia"
config.astromRefObjLoader.ref_dataset_name = config.connections.astromRefCat
config.astromRefObjLoader.anyFilterMapsToThis = "phot_g_mean"
config.astromRefObjLoader.filterMap = {}

# Use panstarrs for photometry (grizy filters).
config.connections.photoRefCat = "panstarrs"
config.photoRefObjLoader.ref_dataset_name = config.connections.photoRefCat
