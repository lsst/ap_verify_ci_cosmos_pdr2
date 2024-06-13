#!/bin/bash
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

# Script for generating a fresh Gen 3 repository in preloaded/. The previous
# contents of the preloaded/ path are removed.


# Abort script on any error
set -e


SCRIPT_DIR="$( dirname -- "${BASH_SOURCE[0]}" )"
REPO_DIR="${SCRIPT_DIR}/../preloaded/"
INST_CLASS=lsst.obs.subaru.HyperSuprimeCam
INST_NAME=HSC


########################################
# Repository creation

rm -rf "$REPO_DIR"
butler create "$REPO_DIR"
butler register-instrument "$REPO_DIR" $INST_CLASS
echo "Created empty $INST_NAME repo in ${REPO_DIR}."


########################################
# Minimal contents

STD_CALIB="${INST_NAME}/calib"
CURATED_CALIB="${STD_CALIB}/curated"

butler write-curated-calibrations "$REPO_DIR" $INST_CLASS \
    --collection "$CURATED_CALIB"
butler collection-chain "$REPO_DIR" "$STD_CALIB" "$CURATED_CALIB"
echo "Added curated calibrations to ${REPO_DIR}."
