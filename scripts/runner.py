import argparse
import gc
import json
import time

def get_identifier():
    parser = argparse.ArgumentParser()
    parser.add_argument("arrayid", type=int, help="ArrayID")
    args = parser.parse_args()
    return "{:04}".format(args.arrayid)

if __name__ == "__main__":
    identifier = get_identifier()

    # Load configuration
    with open("configs/{}.json".format(identifier), "r") as f:
        config = json.load(f)

    # Time execution
    tstart = time.time()

    # TODO: select correct behavior based on "classifier" in config file
    
    # Classifier specific code -------------------------------------------------
    import pandas as pd
    import xgboost as xgb

    # Non classifier specific settings
    settings = config["settings"]

    train_path = settings["train"]
    test_path = settings["test"]

    variables = settings["variables"]
    classlabel = settings["classlabel"]
    weight = settings["weight"]
    
    # Load data
    invars = variables + [classlabel, weight]

    data_train = pd.read_hdf(train_path, columns=invars)
    dtrain = xgb.DMatrix(data_train[variables],
                         label=data_train[classlabel],
                         weight=data_train[weight])
    del data_train
    gc.collect()

    data_test = pd.read_hdf(test_path, columns=invars)
    dtest = xgb.DMatrix(data_test[variables],
                        label=data_test[classlabel],
                        weight=data_test[weight])
    del data_test
    gc.collect()

    # Define samples to monitor
    watchlist = [(dtrain, "train"), (dtest, "test")]

    # Start training
    params = config["classifier_settings"].copy()
    early_stopping_rounds = params.pop("early_stopping_rounds")
    num_rounds = params.pop("num_rounds")

    bst = xgb.train(params, dtrain, num_rounds, watchlist,
                    early_stopping_rounds=early_stopping_rounds)
    bst.save_model("models/{}.model".format(config["identifier"]))

    # End of classifier specific code -----------------------------------------
    
    tend = time.time()

    config["trained"] = True
    config["training_time"] = tend - tstart
    with open("configs/{}.json".format(identifier), "w") as f:
        json.dump(config, f, indent=4)