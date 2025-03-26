Dataset management scripts
==========================

This directory has scripts for (re)creating the `ap_verify_ci_cosmos_pdr2` data set.
This repo does not have a complete set of scripts nor a "regenerate everything" script, but individual files may be run as needed.
The scripts `generate_fake_injection_catalog.sh` and `import_calibs.py` are not self-contained, and the user may need to manually edit chains before or after running them.

*Any* change to the repo requires running `make_preloaded_export.py` to ensure the export file is up-to-date.
The data set will not run correctly without this step, but it also makes it easy to see and review each commit's changes.

See each script's docstring for usage instructions; those scripts that take arguments also support `--help`.

Contents
--------
path                               | description
:----------------------------------|:-----------------------------
generate_ephemerides_gen3.py       | Download solar system ephemerides and register them in `preloaded/`.
generate_fake_injection_catalog.sh | Create source injection catalogs in the COSMOS field. Requires templates.
generate_refcats_gen3.py           | Transfer refcats from an external repo (such as `repo/main`) and register them in `preloaded/`.
generate_self_preload.py           | Create preloaded APDB datasets by simulating a processing run with no pre-existing DIAObjects.
get_nn_models.py                   | Transfer a selected pretrained model from an external repo (such as `repo/main`) and register it in `preloaded/`.
import_calibs.py                   | Transfer calibs from an external repo (such as `repo/main`) and register them in `preloaded/`.
import_templates_gen3.py           | Transfer templates from an external repo (such as `repo/main`) and register them in `preloaded/`.
make_empty_repo.sh                 | Replace `preloaded/` with a repo containing only dimension definitions and standard "curated" calibs.
make_preloaded_export.py           | Create an export file of `preloaded/` that's compatible with `butler import`.
