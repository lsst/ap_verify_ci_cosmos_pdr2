# Config override for lsst.ap.pipe.ApPipeTask
import os.path

configDir = os.path.dirname(__file__)

# Ignore missing calibrations
config.ccdProcessor.isr.load(os.path.join(configDir, 'isr.py'))
