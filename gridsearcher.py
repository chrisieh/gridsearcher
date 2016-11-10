import glob
import itertools
import json
import os


# Build list of option dictionaries from dictionary
def grid_to_opts(grid):
    options = {key: grid[key] if isinstance(grid[key], list) else [grid[key]] for key in grid}
    keys, vals = options.keys(), options.values()
    product = itertools.product(*vals)
    options = [dict(zip(keys, x)) for x in product]
    return options


# Check for existing configs
identifiers = []
for filename in glob.glob("models/*.json"):
    with open(filename, "r") as f:
        config = json.load(f)
    identifiers.append(int(config["identifier"]))

id_start = 0 if len(identifiers) == 0 else max(identifiers) + 1

# TODO: this should be a cmd line argument
with open("config/xgb_template.json") as f:
    config = json.load(f)

options = grid_to_opts(config["grid"])

# Build model description files
for i, opt in enumerate(options, id_start):
    label = "{:04}".format(i)
    
    model_desc = {
        "identifier": "{:04}".format(i),
        "classifier": config["classifier"],
        "settings": config["settings"],
        "classifier_settings": opt,
        "submitted": False,
        "trained": False
    }
    
    with open("models/{}.json".format(label), "w") as f:
        json.dump(model_desc, f, indent=4)