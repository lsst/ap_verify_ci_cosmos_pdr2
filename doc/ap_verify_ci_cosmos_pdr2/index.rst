.. _ap_verify_ci_cosmos_pdr2-package:

########################
ap_verify_ci_cosmos_pdr2
########################

The ``ap_verify_ci_cosmos_pdr2`` package is a minimal collection of images from the HSC `COSMOS`_ survey, formatted for use with :ref:`lsst.ap.verify`.
It is intended as a basic functionality test for the Alert Production pipeline.

.. _COSMOS: https://doi.org/10.1086%2F516585

.. _ap_verify_ci_cosmos_pdr2-using:

Using ap_verify_ci_cosmos_pdr2
==============================

This dataset is designed for "quick and dirty" integration testing of the existing alert production verification tooling.
The input data were chosen arbitrarily, so they are not even suitable for testing of difference imaging analysis.

.. _ap_verify_ci_cosmos_pdr2-contents:

Dataset contents
================

This package provides two partially overlapping images from the same night in the 2016 `COSMOS`_ survey.
It contains:

* CCDs 50 and 51 from visits 59150 and 59160, respectively, from pointing 1527 in the ``SSP_UDEEP_COSMOS`` survey field, in g band.
* biases, darks, brighter-fatter kernals, and g-band flats and sky frames.
* reference catalogs for Gaia and Pan-STARRS1, covering the raw images' footprint.

.. _ap_verify_ci_cosmos_pdr2-contributing:

Contributing
============

``ap_verify_ci_cosmos_pdr2`` is developed at https://github.com/lsst/ap_verify_ci_cosmos_pdr2.
You can find Jira issues for this module under the `ap_verify <https://jira.lsstcorp.org/issues/?jql=project%20%3D%20DM%20AND%20component%20%3D%20ap_verify%20AND%20text~"cosmos PDR2">`_ component.

.. If there are topics related to developing this module (rather than using it), link to this from a toctree placed here.

.. .. toctree::
..    :maxdepth: 1
