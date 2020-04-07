`ap_verify_ci_cosmos_pdr2`
==========================

Data from COSMOS PDR2 to test basic functionality of alert production.

Contains HSC visits arbitrarily chosen from the second data release's ultradeep fields.
Because the data have not been selected in any way, this dataset may not be suitable for scientific validation.

Relevant Files and Directories
------------------------------
path                  | description
:---------------------|:-----------------------------
`doc`                 | Contains Sphinx package documentation for the dataset. This documentation may be linked to from other packages, such as `ap_verify`.
`raw`                 | Raw, compressed HSC fits images from SSP_UDEEP_COSMOS pointing 1527.
`calib`               | To be populated with master calibs. Calibration files do not need to follow a specific subdirectory structure. Currently empty.
`config`              | To be populated with dataset-specific configs. Currently contains an example file corresponding to the contents of `raw` and `refcats`.
`templates`           | To be populated with `TemplateCoadd` images produced by a compatible version of the LSST pipelines. Must be organized as a filesystem-based Butler repo. Currently empty.
`repo`                | A template for a Butler raw data repository. This directory must never be written to; instead, it should be copied to a separate location, and data ingested into the copy (this is handled automatically by `ap_verify`, see below). Currently contains the appropriate HSC `_mapper` file.
`refcats`             | To be populated with tarball(s) of HTM shards from relevant reference catalogs. Currently contains a small (useless) example tarball.
`dataIds.list`        | List of dataIds in this repo. For use in running Tasks. Currently set to run all Ids.


Git LFS
-------

To clone and use this repository, you'll need Git Large File Storage (LFS).

Our [Developer Guide](http://developer.lsst.io/en/latest/tools/git_lfs.html) explains how to setup Git LFS for LSST development.

Usage
-----

`ap_verify_ci_cosmos_pdr2` is designed to be run using [`ap_verify`](https://pipelines.lsst.io/modules/lsst.ap.verify/), which is distributed as part of the `lsst_distrib` package of the [LSST Science Pipelines](https://pipelines.lsst.io/).

This dataset is not included in `lsst_distrib` and is not available through `newinstall.sh`.
However, it can be installed explicitly with the [LSST Software Build Tool](https://developer.lsst.io/stack/lsstsw.html) or by cloning directly:

    git clone https://github.com/lsst/<dataset>/
    setup -r <dataset>

See the Science Pipelines documentation for more detailed instructions on [installing datasets](https://pipelines.lsst.io/modules/lsst.ap.verify/datasets-install.html) and [running `ap_verify`](https://pipelines.lsst.io/modules/lsst.ap.verify/running.html).
