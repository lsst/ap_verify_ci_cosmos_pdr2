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

"""Script for copying calibs appropriate for these exposures.

This script currently requires that the calibration collection be part of a
chained collection, so that it can query the latter to identify the subset of
calibs to export. This restriction should go away after DM-37409.

Example:
$ python import_calibs.py -c "u/me/DM-123456-calib-chain"
imports image calibrations from (the calibration collections in)
u/me/DM-123456-calib in /repo/main to calibs in this dataset's preloaded repo.
"""

import argparse
import logging
import os
import sys
import tempfile

import lsst.log
import lsst.skymap
from lsst.daf.butler import Butler, CollectionType


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
lsst.log.configure_pylog_MDC("DEBUG", MDC_class=None)


# raw-like data IDs used to query for calibs, since we can't query them directly.
DATA_IDS = [dict(instrument="HSC", visit=59134, detector=0),
            dict(instrument="HSC", visit=59134, detector=4),
            dict(instrument="HSC", visit=59134, detector=5),
            dict(instrument="HSC", visit=59142, detector=0),
            dict(instrument="HSC", visit=59142, detector=5),
            dict(instrument="HSC", visit=59142, detector=11),
            dict(instrument="HSC", visit=59150, detector=50),
            dict(instrument="HSC", visit=59150, detector=58),
            dict(instrument="HSC", visit=59160, detector=43),
            dict(instrument="HSC", visit=59160, detector=51),
            ]
CALIB_NAMES = ["bias", "dark", "flat"]

# Avoid explicit references to dataset package to maximize portability.
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
DATASET_REPO = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "preloaded"))
DATASET_CALIB_COLLECTION = "HSC/calib"


########################################
# Command-line options

def _make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="src_dir", default="/repo/main",
                        help="Repo to import from, defaults to '/repo/main'.")
    parser.add_argument("-c", dest="src_collection", required=True,
                        help="Calib collection to import from. Must be a chained collection before DM-37409.")
    return parser


args = _make_parser().parse_args()


########################################
# Export/Import

def _export(butler, export_file):
    """Export the files to be copied.

    Parameters
    ----------
    butler : `lsst.daf.butler.Butler`
        A Butler pointing to the repository and collection(s) to be
        exported from.
    export_file : `str`
        A path pointing to a file to contain the export results.

    Returns
    -------
    calib_collections : iterable [`str`]
        The names of the calibration collections containing validities.
    """
    with butler.export(filename=export_file, transfer=None) as contents:
        for data_id in DATA_IDS:
            calibs = butler.registry.queryDatasets(CALIB_NAMES, dataId=data_id,
                                                   collections=butler.collections)
            contents.saveDatasets(calibs)

        calib_collections = set()
        for collection in butler.collections:
            calib_collections.update(_save_validities(butler.registry, contents, collection))
        return calib_collections


def _save_validities(registry, exporter, collection):
    """Transfer the validity information found in a collection or any of its
    sub-collections.

    This function is guaranteed not to add any datasets to the exporter.

    Parameters
    ----------
    registry : `lsst.daf.butler.Registry`
        The registry managing the collections.
    exporter : `lsst.daf.butler.transfers.RepoExportContext`
        The export manager to which to copy validities.
    collection : `str`
        The collection from which to copy validities.

    Returns
    -------
    calib_collections : iterable [`str`]
        All the individual calibration collections that were exported.
    """
    match registry.getCollectionType(collection):
        case CollectionType.CALIBRATION:
            exporter.saveCollection(collection)
            return {collection}
        case CollectionType.CHAINED:
            calib_collections = set()
            for child in registry.getCollectionChain(collection):
                calib_collections.update(_save_validities(registry, exporter, child))
            return calib_collections
        case _:
            return []


def _import(butler, export_file, base_dir):
    """Import the exported files.

    Parameters
    ----------
    butler : `lsst.daf.butler.Butler`
        A Butler pointing to the dataset repository.
    export_file : `str`
        A path pointing to a file containing the export results.
    base_dir : `str`
        The base directory for the file locations in ``export_file``.
    """
    butler.import_(directory=base_dir, filename=export_file, transfer="copy")


with tempfile.NamedTemporaryFile(suffix=".yaml") as export_file:
    src = Butler(args.src_dir, collections=args.src_collection, writeable=False)
    calib_collections = _export(src, export_file.name)
    dest = Butler(DATASET_REPO, writeable=True)
    _import(dest, export_file.name, args.src_dir)
    dest.registry.registerCollection(DATASET_CALIB_COLLECTION, CollectionType.CHAINED)
    chain = list(dest.registry.getCollectionChain(DATASET_CALIB_COLLECTION))
    chain.extend(calib_collections)
    dest.registry.setCollectionChain(DATASET_CALIB_COLLECTION, chain)

logging.info(f"Calibs stored in {DATASET_REPO}:{DATASET_CALIB_COLLECTION}.")
