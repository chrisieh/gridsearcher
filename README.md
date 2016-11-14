# README

## Caveats

Currently only `XGBoost` supported.

## Requirements

Python packages for running on the cluster (virtualenv strongly recommended):
- `numpy` (pip)
- `pandas` (pip)
- `tables` (pip)
- `xgboost` ([compile](http://xgboost.readthedocs.io/en/latest/build.html) from source)
- `sklearn` (pip)

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