#!/usr/bin/env python
# This file is part of ap_verify_ci_cosmos_pdr2.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Script for copying standard refcats that cover this dataset's fields.

Running this script allows for updates to the refcats to be incorporated
into the dataset.
"""

import argparse
import logging
import sys

from astropy.coordinates import SkyCoord

import lsst.log
import lsst.sphgeom
from lsst.daf.butler import Butler, CollectionType, DatasetRef, DatasetType, FileDataset


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
lsst.log.configure_pylog_MDC("DEBUG", MDC_class=None)


########################################
# Fields and catalogs to process

# Use SkyCoord because it provides built-in sexagecimal and HMS support.
FIELDS = [SkyCoord("10h00m28.800s", "+02d12m36.00s"),  # field 26 (2014:04)
          SkyCoord("10h20m28.800s", "-06d31m12.00s"),  # field 40 (2014:10)
          SkyCoord("10h21m52.800s", "-04d57m00.00s"),  # field 42 (2014:09)
          ]
FIELD_RADIUS = 2.0  # degrees

# Key is catalog name in source repo, value is name in ap_verify_ci_cosmos_pdr2.
REFCATS = {"gaia_dr2_20200414": "gaia",
           "ps1_pv3_3pi_20170110": "panstarrs",
           }


########################################
# Command-line options

def _make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="src_dir", default="/repo/main",
                        help="Refcat source Butler repo, defaults to '/repo/main'.")
    parser.add_argument("-i", dest="src_collection", default="refcats",
                        help="Refcat source collection, defaults to 'refcats'.")
    return parser


args = _make_parser().parse_args()


########################################
# Identify all required shards

HTM_LEVEL = 7


def _get_shards(centers, radius):
    """Return all shards overlapping a set of fields.

    Parameters
    ----------
    centers : iterable [`astropy.coordinates.SkyCoord`]
        The right ascension and declination of the field centers.
    radius : `float`
        The radius of each field, in degrees.

    Returns
    -------
    shards : iterable [`tuple` [`int`]]
        The ranges of consecutive HTM indices that overlap any of the fields.
        Individual ranges may overlap. Each range is represented as a tuple of
        the lowest and the highest index in the range, inclusive (thus, an
        isolated index ``i`` is represented by ``(i, i)``).
    """
    indexer = lsst.sphgeom.HtmPixelization(HTM_LEVEL)
    shards = []
    for center in centers:
        vector = center.represent_as('cartesian').xyz.value
        region = lsst.sphgeom.Circle(lsst.sphgeom.UnitVector3d(vector[0], vector[1], vector[2]),
                                     lsst.sphgeom.Angle.fromDegrees(radius))
        # Convert from half-open to fully-closed intervals.
        shards.extend((start, end-1) for (start, end) in indexer.envelope(region))
    return shards


logging.info("Identifying refcat shards...")
shards = _get_shards(FIELDS, FIELD_RADIUS)
if not shards:
    raise RuntimeError("No HTM shards found; coordinates are likely corrupted.")
logging.debug("%d shard ranges found", len(shards))


def _make_range(start, end):
    """Represent a range of contiguous integers in Butler dimension
    expression syntax.

    Parameters
    ----------
    start, end : `int`
        The first and last elements of the range, *inclusive*.
        Assumes ``start <= end``.

    Returns
    -------
    range : `str`
        The Butler syntax for the range.
    """
    if start == end:
        return str(start)
    else:
        return f"{start}..{end}"


id_ranges = [_make_range(start, end) for (start, end) in shards]


########################################
# Transfer shards

DEST_DIR = "${AP_VERIFY_CI_COSMOS_PDR2_DIR}/preloaded/"
STD_REFCAT = "refcats"
DEST_RUN = "refcats/imported"


def _rename_dataset_type(type, name):
    """Create a DatasetType that differs from an existing one in name only.

    Parameters
    ---------
    type : `lsst.daf.butler.DatasetType`
        The type to rename.
    name : `str`
        The new name to adopt.

    Returns
    -------
    new_type : `lsst.daf.butler.DatasetType`
        The new DatasetType.
    """
    return DatasetType(name, type.dimensions, type.storageClass, type.parentStorageClass)


src_repo = Butler(args.src_dir, collections=args.src_collection, writeable=False)
dest_repo = Butler(DEST_DIR, run=DEST_RUN, writeable=True)


def _remove_refcat_run(butler, run):
    """Remove a refcat run and any references from a repository.

    Parameters
    ----------
    butler : `lsst.daf.butler.Butler`
        The repository from which to remove ``run``.
    run : `str`
        The run to remove, if it exists.
    """
    try:
        refcat_runs = butler.registry.getCollectionChain(STD_REFCAT)
        if run in refcat_runs:
            new_runs = list(refcat_runs)
            new_runs.remove(run)
            butler.registry.setCollectionChain(STD_REFCAT, new_runs)
    except (lsst.daf.butler.MissingCollectionError, TypeError):
        pass  # No STD_REFCAT chain; nothing to do

    try:
        butler.removeRuns([run], unstore=True)
    except lsst.daf.butler.MissingCollectionError:
        pass  # Already removed; nothing to do


logging.info("Preparing destination repository %s...", DEST_DIR)
_remove_refcat_run(dest_repo, DEST_RUN)
dest_repo.registry.registerCollection(DEST_RUN, CollectionType.RUN)
for src_cat, dest_cat in REFCATS.items():
    src_type = src_repo.registry.getDatasetType(src_cat)
    dest_type = _rename_dataset_type(src_type, dest_cat)
    dest_repo.registry.registerDatasetType(dest_type)
dest_repo.registry.refresh()

logging.info("Searching for refcats in %s:%s...", args.src_dir, args.src_collection)
query = f"htm{HTM_LEVEL} in ({','.join(id_ranges)})"
datasets = []
for src_ref in src_repo.registry.queryDatasets(REFCATS.keys(), where=query, findFirst=True):
    src_type = src_ref.datasetType
    dest_type = _rename_dataset_type(src_type, REFCATS[src_type.name])
    dest_ref = DatasetRef(dest_type, src_ref.dataId)
    datasets.append(FileDataset(path=src_repo.getURI(src_ref), refs=dest_ref))

logging.info("Copying refcats...")
dest_repo.ingest(*datasets, transfer="copy")

logging.info("%d refcat shards copied to %s:%s", len(datasets), DEST_DIR, DEST_RUN)
