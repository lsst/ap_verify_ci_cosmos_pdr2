Dataset management scripts
==========================

This directory has scripts for (re)creating the `ap_verify_ci_cosmos_pdr2` data set.
This repo does not have a complete set of scripts nor a "regenerate everything" script, but individual files may be run as needed.
The script `import_calibs.py` is not self-contained, and the user may need to manually edit chains before or after running it.

`generate_self_preload.py` now includes fake-catalog generation and sharding as part of its workflow.
For routine regeneration, prefer `generate_self_preload.py` and treat `generate_fake_injection_catalog.sh` as deprecated.

`scripts/generate_self_preload.py` now performs three steps in sequence when regenerating preload products:

1. Run the AP pipeline (`ApPipe.yaml`) to produce DIA preload catalogs.
2. Run fake-catalog generation (`CreateInjectionCatalogs.yaml`).
3. Shard fake catalogs with `ap_pipe/scripts/fakes/shard_fake_catalogs.py`.

This means fake injection catalogs are produced as part of the same self-preload workflow.
The standalone script `scripts/generate_fake_injection_catalog.sh` should be treated as deprecated for routine dataset regeneration.


*Any* change to the repo requires running `make_preloaded_export.py` to ensure the export file is up-to-date.
The data set will not run correctly without this step, but it also makes it easy to see and review each commit's changes.

See each script's docstring for usage instructions; those scripts that take arguments also support `--help`.

Contents
--------
path                               | description
:----------------------------------|:-----------------------------
generate_ephemerides_gen3.py       | Download solar system ephemerides and register them in `preloaded/`.
generate_fake_injection_catalog.sh | DEPRECATED for routine use; fake catalog generation and sharding are handled by `generate_self_preload.py`.
generate_refcats_gen3.py           | Transfer refcats from an external repo (such as `repo/main`) and register them in `preloaded/`.
generate_self_preload.py           | Create preloaded APDB datasets by simulating a processing run with no pre-existing DIAObjects, then generate and shard fake injection catalogs.
get_nn_models.py                   | Transfer a selected pretrained model from an external repo (such as `repo/main`) and register it in `preloaded/`.
import_calibs.py                   | Transfer calibs from an external repo (such as `repo/main`) and register them in `preloaded/`.
import_templates_gen3.py           | Transfer templates from an external repo (such as `repo/main`) and register them in `preloaded/`.
make_empty_repo.sh                 | Replace `preloaded/` with a repo containing only dimension definitions and standard "curated" calibs.
make_preloaded_export.py           | Create an export file of `preloaded/` that's compatible with `butler import`.
