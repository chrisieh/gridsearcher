import glob
import json
import os
import subprocess
import sys


def set_key(files, key, value):
    for filename in files:
        with open(filename) as f:
            config = json.load(f)
        
        config[key] = value
        with open(filename, "w") as f:
            json.dump(config, f, indent=4)


def submit(args):
    base_dir = os.path.dirname(args.script)
    config_dir = os.path.join(base_dir, "configs")

    if args.train:
        submitted = "submitted_train"
    if args.eval:
        submitted = "submitted_eval"

    # Find jobs which have not been submitted
    not_submitted = []
    for filename in glob.glob(os.path.join(config_dir, "*.json")):
        with open(filename) as f:
            config = json.load(f)
        if not config[submitted]:
            not_submitted.append((filename, config["identifier"]))
    
    if len(not_submitted) == 0:
        print("Nothing to submit")
        sys.exit(0)
    
    # Select jobs to submit
    if args.n is not None and len(not_submitted) > args.n:
        submit = not_submitted[:args.n]
    else:
        submit = not_submitted
    
    qsub_t_str = ",".join(map(str, [int(identifier) for _, identifier in submit]))
    
    print("Submitting: {}".format(qsub_t_str))
    retcode = subprocess.call(["qsub", "-d", base_dir,
                               "-t", qsub_t_str,
                               os.path.basename(args.script)])

    # Set submitted to true
    if retcode == 0:
        set_key([filename for filename, _ in submit], submitted, True)
    
    sys.exit(retcode)
