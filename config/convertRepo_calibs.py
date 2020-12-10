# Config overrides for convert_gen2_repo_to_gen3.py

config.datasetIgnorePatterns = ["raw", "*Coadd_skyMap", "ref_cat", "defects"]
# Suppress auto-conversion of skymaps; it causes trouble for the template repo
config.rootSkyMapName = None

# Already stored in convertRepo_templates.py
config.doRegisterInstrument = False

# Work around HSC defaults assuming HSC/masks must exist
config.extraUmbrellaChildren = []
