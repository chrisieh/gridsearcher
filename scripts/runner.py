import argparse
import json
import gc

def get_identifier():
    parser = argparse.ArgumentParser()
    parser.add_argument("arrayid", type=int, help="ArrayID")
    args = parser.parse_args()
    return "{:04}".format(args.arrayid)

if __name__ == "__main__":
    identifier = get_identifier()

    with open(identifier + ".json", "r") as f:
        config = json.load(f)
    
    # Classifier specific code -------------------------------------------------
    import pandas as pd
    import xgboost as xgb
    
    # Load data
    invars = config["variables"] + [config["weight"], config["classlabel"]]
    data_train = pd.read_hdf(config["train"], columns=invars)
    dtrain = xgb.DMatrix(data_train[config["variables"]],
                         label=data_train[config["classlabel"]],
                         weight=data_train[config["weight"]])    
    # Free memory
    del data_train
    gc.collect()

    data_test = pd.read_hdf(config["test"], columns=invars)
    dtest = xgb.DMatrix(data_test[config["variables"]],
                        label=data_test[config["classlabel"]],
                        weight=data_test[config["weight"]])
    # Free memory
    del data_test
    gc.collect()

    evallist = [(dtrain, "train"), (dtest, "test")]

    # TODO: move this to json?
    params = config["config"].copy()
    params["eval_metric"] = ["auc", "rmse"]
    params["nthread"] = 8
    num_rounds = 20
    early_stopping = 20

    bst = xgb.train(params, dtrain, num_rounds, evallist,
                    early_stopping_rounds=early_stopping)
    bst.save_model("{}.model".format(config["identifier"]))
    # End of classifier specific code -----------------------------------------
    
    config["processed"] = True
    with open(identifier + ".json", "w") as f:
        json.dump(config, f, indent=4)