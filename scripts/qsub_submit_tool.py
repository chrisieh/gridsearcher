import argparse
import glob
import json
import subprocess
import sys

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, help="Number of jobs")
    parser.add_argument("script", help="Path to PBS script")
    return parser.parse_args()


def set_submitted(files):
    for filename in files:
        with open(filename) as f:
            config = json.load(f)
        
        config["submitted"] = True
        with open(filename, "w") as f:
            json.dump(config, f, indent=4)


if __name__ == "__main__":
    args = get_args()
    base_dir = os.path.dirname(args.script)
    config_dir = os.path.join(base_dir, "configs")

    # Find jobs which have not been submitted
    not_submitted = []
    for filename in glob.glob(os.path.join(config_dir, "*.json")):
        with open(filename) as f:
            config = json.load(f)
        if not config["submitted"]:
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
    retcode = subprocess.call(["qsub", "-d", base_dir,"-t", qsub_t_str, args.script])

    # Set submitted to true
    if retcode == 0:
        set_submitted([filename for filename, _ in submit])
    
    sys.exit(retcode)
