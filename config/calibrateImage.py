# Config override for lsst.pipe.tasks.calibrateImage.CalibrateImageTask
# Ensure we're using the refcats that are actually in this dataset, regardless
# of what task defaults are.
import os.path
import lsst.utils
hsc_config_dir = os.path.join(lsst.utils.getPackageDir("obs_subaru"), "config")

# Use ps1 for astrometry (the HSC default).
config.connections.astrometry_ref_cat = "ps1_pv3_3pi_20170110"
config.astrometry_ref_loader.load(os.path.join(hsc_config_dir, "filterMap.py"))
# Use the filterMap instead of the "any" filter (as is used for Gaia).
config.astrometry_ref_loader.anyFilterMapsToThis = None

# Use panstarrs for photometry (the HSC default).
config.connections.photometry_ref_cat = "ps1_pv3_3pi_20170110"
