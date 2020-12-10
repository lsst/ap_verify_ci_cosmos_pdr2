# Config overrides for convert_gen2_repo_to_gen3.py

config.datasetIncludePatterns = ["ref_cat", "defects"]

config.refCats = ['gaia', 'panstarrs']
for refcat in config.refCats:
    config.runs[refcat] = "refcats"

# Already stored in convertRepo_templates.py
config.doRegisterInstrument = False

# Work around HSC defaults assuming HSC/masks must exist
config.extraUmbrellaChildren = []
