# README

## Caveats

- Currently only `XGBoost` supported
- Training and testing sample needs to be in HDF5 format and signal/background need
  to be merged into a single sample with a flag (e.g. is_sig) indicating whether it is
  signal or background (for an example see `scripts/PrepareSample.ipynb` requires `root_numpy`)

## Requirements

Python packages for running on the cluster (virtualenv strongly recommended):
- `numpy` (pip)
- `pandas` (pip)
- `tables` (pip)
- `xgboost` ([compile](http://xgboost.readthedocs.io/en/latest/build.html) from source)
- `sklearn` (pip)

For collecting the results of the evaluation:
- `jupyter` (for the notebook)

## Quickstart

Create a project folder for the grid-search:

    python gridsearcher.py init [--xgb] [--pbs] folder

The `--xgb`/`--pbs` flags copy templates for XGBoost and a PBS script for
submission to the cluster into the project directory `folder`.

Modify the templates and build the configuration files for the different
trainings:

    python gridsearcher.py build xgb_grid.json

This creates all the model configurations in the `configs` folder of the
project folder.

Submit a number of training jobs `-n <num. of jobs>` to the cluster for training
`--train` or evaluation `--eval`:

    python gridsearcher.py submit --train [-n N] pbs_train.sh

Analogous for evaluation (sends only trained jobs to the cluster):

    python gridsearcher.py submit --eval [-n N] pbs_eval.sh
