import glob
import itertools
import json
import os


# Build list of option dictionaries from configuration file
def get_options(filename):
    with open(filename)as f:
        config = json.load(f)

    # Build list of options for non-common options
    options = {key: config[key] if isinstance(config[key], list) else [config[key]] for key in config}
    keys, vals = options.keys(), options.values()
    product = itertools.product(*vals)
    options = [dict(zip(keys, x)) for x in product]
    
    return options


# TauID variables
tid_1pvars = ["TauJets.centFrac", "TauJets.etOverPtLeadTrk",
              "TauJets.innerTrkAvgDist", "TauJets.absipSigLeadTrk",
              "TauJets.SumPtTrkFrac", "TauJets.ChPiEMEOverCaloEME",
              "TauJets.EMPOverTrkSysP", "TauJets.ptRatioEflowApprox",
              "TauJets.mEflowApprox"]

tid_3pvars = ["TauJets.centFrac", "TauJets.etOverPtLeadTrk",
              "TauJets.innerTrkAvgDist", "TauJets.dRmax",
              "TauJets.trFlightPathSig", "TauJets.massTrkSys",
              "TauJets.ChPiEMEOverCaloEME", "TauJets.EMPOverTrkSysP",
              "TauJets.ptRatioEflowApprox", "TauJets.mEflowApprox"]

# User input -------------------------------------------------------------------

# Input sample configuration
train = "samples/train.h5"
test = "samples/test.h5"

# Grid-search configuration
options = []
options.extend(get_options("config/xgb_template.json"))
#options.extend(get_options("config/mycustomgrid.json"))

# Variable selection
variables = tid_1pvars
weight = "weight"
classlabel = "is_sig"

batch_settings = {"name": "GridSearcher", "workdir": os.path.abspath("models"),
                  "req_mem": "4g", "req_file": "10g", "queue": "medium",
                  "runner": os.path.abspath("scripts/runner.py")}

# End user input ---------------------------------------------------------------

# Check for existing configs
identifiers = []
for filename in glob.glob("models/*.json"):
    with open(filename, "r") as f:
        config = json.load(f)
    identifiers.append(int(config["identifier"]))

id_start = 0 if len(identifiers) == 0 else max(identifiers) + 1

# Build model description files
for i, opt in enumerate(options, id_start):
    label = "{:04}".format(i)
    
    model_desc = {"identifier": "{:04}".format(i),
                  "train": os.path.abspath(train),
                  "test": os.path.abspath(test),
                  "variables": variables,
                  "weight": weight,
                  "classlabel": classlabel,
                  "config": opt,
                  "submitted": False,
                  "processed": False}
    
    with open("models/{}.json".format(label), "w") as f:
        json.dump(model_desc, f, indent=4)

# Build PBS script for batch submission
with open("config/pbs_template.sh", "r") as f:
    pbs_script = f.read()

with open("scripts/pbs.sh", "w") as f:
    f.write(pbs_script.format(**batch_settings))
    f.write("## Do not change - this file is automagically generated")