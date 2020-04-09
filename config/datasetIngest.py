# Config override for lsst.ap.verify.ingestion.DatasetIngestTask

config.refcats = {
    'gaia': 'gaia_cosmos_2016.tar.gz',
    'panstarrs': 'panstarrs_cosmos_2016.tar.gz'
}

# Workaround for DM-24395
config.defectIngester.register.visit = ['calibDate', 'filter']
