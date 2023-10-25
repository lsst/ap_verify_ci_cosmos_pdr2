`ap_verify_ci_cosmos_pdr2`
==========================

Data from the 2016 COSMOS survey, processed in the PDR2 run in May 2019, to test basic functionality of alert production.

https://hsc-release.mtk.nao.ac.jp/doc/index.php/sample-page/pdr2/

Contains HSC visits arbitrarily chosen from the second data release's ultradeep fields (`tract=9813` with `skymap=hsc_rings_v1`), from pointing 1527 in the `SSP_UDEEP_COSMOS` field.
Because the data have not been selected in any way, this dataset may not be suitable for scientific validation.
This dataset contains the following dataIds, both in the HSC-G filter:

* visit 59134, detectors 0, 4, 5
* visit 59142, detectors 0, 5, 11
* visit 59150, detectors 50, 58
* visit 59160, detectors 43, 51

Relevant Files and Directories
------------------------------
path                  | description
:---------------------|:-----------------------------
`doc`                 | Contains Sphinx package documentation for the dataset. This documentation may be linked to from other packages, such as `ap_verify`.
`raw`                 | Raw, compressed HSC fits images from SSP_UDEEP_COSMOS pointing 1527.
`config`              | Dataset-specific configs to help Stack code work with this dataset.
`pipelines`           | Dataset-specific pipelines to run on this dataset.
`dataIds.list`        | List of dataIds in this repo. For use in running Tasks. Currently set to run all Ids.
`preloaded`           | A Gen 3 Butler repository containing HSC master calibs from the 2016 COSMOS campaign (or, where necessary, from 2015), coadded images for use as differencing templates, and PS1 reference catalog in HTM format for regions overlapping any visit in the dataset.
`scripts`             | Scripts and data for generating this dataset.


Git LFS
-------

To clone and use this repository, you'll need Git Large File Storage (LFS).

Our [Developer Guide](http://developer.lsst.io/en/latest/tools/git_lfs.html) explains how to setup Git LFS for LSST development.

Usage
-----

`ap_verify_ci_cosmos_pdr2` is designed to be run using [`ap_verify`](https://pipelines.lsst.io/modules/lsst.ap.verify/), which is distributed as part of the `lsst_distrib` package of the [LSST Science Pipelines](https://pipelines.lsst.io/).

This dataset is not included in `lsst_distrib` and is not available through `newinstall.sh`.
However, it can be installed explicitly with the [LSST Software Build Tool](https://developer.lsst.io/stack/lsstsw.html) or by cloning directly:

    git clone https://github.com/lsst/ap_verify_ci_cosmos_pdr2/
    setup -r ap_verify_ci_cosmos_psr2

See the Science Pipelines documentation for more detailed instructions on [installing datasets](https://pipelines.lsst.io/modules/lsst.ap.verify/datasets-install.html) and [running `ap_verify`](https://pipelines.lsst.io/modules/lsst.ap.verify/running.html).
