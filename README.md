# README

## Quickstart

1. Clone this repo
2. Optional: Place training/test sample in `samples`-folder
3. Setup grid, samples, classifier settings in `templates/xgb_template.json`
4. Setup PBS script `templates/pbs_template.sh` for cluster submission
5. Create model descriptions `python scripts/gridsearcher.py templates/xgb_template.json`
6. Submit to cluster `python scripts/qsub_submit_tool.py -n <number of jobs> templates/pbs_template.json`
