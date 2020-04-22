# Config override for lsst.ap.pipe.ApPipeTask
import os.path

configDir = os.path.dirname(__file__)

# Ignore missing calibrations
config.ccdProcessor.isr.load(os.path.join(configDir, 'isr.py'))

# Use dataset's reference catalogs
config.ccdProcessor.calibrate.load(os.path.join(configDir, 'calibrate.py'))

# Use dataset's specific templates
config.differencer.load(os.path.join(configDir, 'imageDifference.py'))
