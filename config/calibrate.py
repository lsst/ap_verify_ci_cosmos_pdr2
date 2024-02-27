# Config override for lsst.pipe.tasks.calibrate.CalibrateTask
# Ensure we're using the refcats that are actually in this dataset, regardless
# of what task defaults are.
import os.path

from lsst.utils import getPackageDir

hscDir = os.path.join(getPackageDir("obs_subaru"), "config")

# Use ps1 for astrometry (the HSC default).
config.connections.astromRefCat = "ps1_pv3_3pi_20170110"
config.astromRefObjLoader.load(os.path.join(hscDir, "filterMap.py"))
# Use the filterMap instead of the "any" filter (as is used for Gaia).
config.astromRefObjLoader.anyFilterMapsToThis = None

# Use panstarrs for photometry (grizy filters).
config.connections.photoRefCat = "ps1_pv3_3pi_20170110"
