import argparse
import gc
import json
import os
import time

import numpy as np
import xgboost as xgb
from scipy.interpolate import interp1d

import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve


def get_identifier():
    parser = argparse.ArgumentParser()
    parser.add_argument("arrayid", type=int, help="ArrayID")
    args = parser.parse_args()
    return "{:04}".format(args.arrayid)


def rej_fixed_eff(truth, score, weight, efficiencies):
    fpr, tpr, thr = roc_curve(truth, score, sample_weight=weight)
    nonzero = (fpr != 0)
    eff = tpr[nonzero]
    rej = 1.0 / fpr[nonzero]
    interpol = interp1d(eff, rej, copy=False, bounds_error=False)
    return interpol(efficiencies)


if __name__ == "__main__":
    identifier = get_identifier()
    tstart = time.time()

    # Load config
    with open("configs/{}.json".format(identifier)) as f:
        config = json.load(f)
    
    # Check trained
    if not config["trained"]:
        print("Classifier not trained")
        sys.exit(1)

    model = "models/{}.model".format(identifier)

    # Check modelfile exists
    if not os.path.exists(model):
        print("Model file not found in path: {}".format(model))
        sys.exit(1)

    # Check evaluated
    if config["evaluated"]:
        print("Classifier already evaluated")
        sys.exit(1)

    # Test sample configurations
    settings = config["settings"]
    test_sample = settings["test"]
    invars = settings["variables"]
    weight = settings["weight"]
    classlabel = settings["classlabel"]

    # Load samples
    test_sample = pd.read_hdf(test_sample, columns=invars+[weight, classlabel])
    test_weights = test_sample[weight]
    test_is_sig = test_sample[classlabel]
    dtest = xgb.DMatrix(test_sample[invars], label=test_sample[classlabel],
                        weight=test_sample[weight])
    del test_sample
    gc.collect()

    # Evaluate booster
    bst = xgb.Booster(model_file=model)

    # Best iteration stats
    best_it = int(bst.attr("best_iteration"))
    total_time = config["training_time"] / 3600.0 # hours
    print("Best iteration: {}".format(best_it))
    print("Time: {} h\n".format(total_time))

    # Aggregate results
    results = []

    # In steps of 10% to best_iteration
    check_it = np.linspace(int(0.1 * best_it), best_it, 10, dtype=np.int32)
    for it in check_it:
        # Store settings
        store = config["classifier_settings"].copy()
        store["identifier"] = identifier

        # Number of iterations
        store["best_iteration"] = best_it
        store["iteration"] = int(it)

        # Calculate metrics
        metrics = {}

        print("Checking iteration: {}".format(it))

        # Approx. training time for intermediate step
        train_time = it / float(best_it) * total_time
        print("Time: {} h\n".format(train_time))
        metrics["train_time"] = train_time

        # Evaluate BDT
        scores = bst.predict(dtest, ntree_limit=int(it))

        # Rejection at fixed efficiencies
        rej3, rej5, rej7 = rej_fixed_eff(test_is_sig, scores, test_weights,
                                         [0.3, 0.5, 0.7])
        print("rej. @0.3: {}".format(rej3))
        print("rej. @0.5: {}".format(rej5))
        print("rej. @0.7: {}\n".format(rej7))
        metrics["rej3"] = rej3
        metrics["rej5"] = rej5
        metrics["rej7"] = rej7

        # Area under ROC-curve
        roc_auc = roc_auc_score(test_is_sig, scores, sample_weight=test_weights)
        print("roc-auc.: {}\n".format(roc_auc))
        metrics["roc_auc"] = roc_auc

        store.update(metrics)
        results.append(store)
    
    # Save settings & metrics
    result_file = "evals/{}.csv".format(identifier)
    results = pd.DataFrame(results)
    results.to_csv(result_file, index=False)

    # Set evaluated  
    config["evaluated"] = True
    with open("configs/{}.json".format(identifier), "w") as f:
        json.dump(config, f, indent=4)
    
    tend = time.time()
    eval_time = (tend - tstart) / 60.0 # min
    print("Total evaluation time: {} min\n\n".format(eval_time))
