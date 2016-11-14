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


def build(args):
    base_dir = os.path.dirname(args.config)
    config_dir = os.path.join(base_dir, "configs")

    # Check for existing configs
    identifiers = []
    for filename in glob.glob(os.path.join(config_dir, "*.json")):
        with open(filename, "r") as f:
            config = json.load(f)
        identifiers.append(int(config["identifier"]))

    id_start = 0 if len(identifiers) == 0 else max(identifiers) + 1

    # Load config
    with open(args.config) as f:
        config = json.load(f)

    # Get all combinations of options
    options = grid_to_opts(config["grid"])

    # Build model description files
    for i, opt in enumerate(options, id_start):
        label = "{:04}".format(i)
        
        model_desc = {
            "identifier": "{:04}".format(i),
            "classifier": config["classifier"],
            "settings": config["settings"],
            "classifier_settings": opt,
            "submitted_train": False,
            "trained": False,
            "submitted_eval": False,
            "evaluated": False
        }
        
        with open(os.path.join(config_dir, "{}.json".format(label)), "w") as f:
            json.dump(model_desc, f, indent=4)
