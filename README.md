# README

## Quickstart

1. Clone this repo
2. Optional: Place training/test sample in `samples`-folder
3. Setup grid, samples, classifier settings in `config/xgb_template.json`
4. Setup PBS script `pbs_template.sh` for cluster submission
5. Create model descriptions `python gridsearcher.py config/xgb_template.json`
6. Submit to cluster `python scripts/qsub_submit_tool.py -n <number of jobs> config/pbs_template.json`
