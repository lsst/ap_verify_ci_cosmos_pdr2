#!/usr/bin/env python

"""Extract the htm pixels for the HSC refcats on lsst-dev and tarball them.

Run on lsst-dev, in the directory you want the output to land in, with:
    python trim_catalogs.py
"""

import os
import shutil
import tarfile

from esutil import htm

catalogs = {'gaia_cosmos_2016': '/datasets/hsc/repo/ref_cats/gaia_dr2_20200414/',
            'panstarrs_cosmos_2016': '/datasets/hsc/repo/ref_cats/ps1_pv3_3pi_20170110/',
           }
fields = {(59150, 50): (149.8594, 2.2225),
         }

indexer = htm.HTM(depth=7) 
shards = []
for ra, dec in fields.values():
    # Search for shards within 2 degrees to ensure we have good coverage
    shards += list(indexer.intersect(ra, dec, 2., True))

for name, location in catalogs.items():
    os.mkdir(name)
    shutil.copy(os.path.join(location, 'config.py'), name)
    shutil.copy(os.path.join(location, 'master_schema.fits'), name)
    for shard in shards:
        file = f"{shard}.fits"
        print(f"Copying {os.path.join(file)} to {name}/...")
        shutil.copy(os.path.join(location, file), name)
    with tarfile.open(f"{name}.tar.gz", mode="x:gz", dereference=True) as tar:
        print(f"Packaging {name}.tar.gz...")
        # tar file must not have subdirectories
        olddir = os.getcwd()
        try:
            os.chdir(name)
            for file in os.listdir():
                tar.add(file)
        finally:
            os.chdir(olddir)
