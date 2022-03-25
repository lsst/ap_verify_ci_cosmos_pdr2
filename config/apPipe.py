# Config override for lsst.ap.pipe.ApPipeTask
import os.path

configDir = os.path.dirname(__file__)

# Ignore missing calibrations
config.ccdProcessor.isr.load(os.path.join(configDir, 'isr.py'))

# Use dataset's reference catalogs
config.ccdProcessor.calibrate.load(os.path.join(configDir, 'calibrate.py'))

# Use dataset's specific templates
config.retrieveTemplate.load(os.path.join(configDir, 'retrieveTemplate.py'))
config.differencer.load(os.path.join(configDir, 'imageDifference.py'))
config.transformDiaSrcCat.load(os.path.join(configDir, 'transformDiaSrcCat.py'))
config.diaPipe.load(os.path.join(configDir, 'diaPipe.py'))
