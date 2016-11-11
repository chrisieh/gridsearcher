import argparse
import os
import shutil
import sys

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Project folder")
    parser.add_argument("-xgb", action="store_true",
                        help="Copy XGBoost templates")
    parser.add_argument("-pbs", action="store_true",
                        help="Copy PBS templates")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    
    if os.path.exists(args.folder):
        print("Path already exists")
        sys.exit(1)
    
    # Create folder skeleton
    os.mkdir(args.folder)
    os.mkdir(os.path.join(args.folder, "models"))
    os.mkdir(os.path.join(args.folder, "configs"))
    os.mkdir(os.path.join(args.folder, "evals"))
    os.mkdir(os.path.join(args.folder, "scripts"))

    # Copy templates
    script_dir, _ = os.path.split(__file__)
    root_dir, _ = os.path.split(script_dir)
    template_dir = os.path.join(root_dir, "templates")

    if args.xgb:
        fname = "xgb_template.json"
        shutil.copy2(os.path.join(template_dir, fname),
                     os.path.join(args.folder, fname))
    
    if args.pbs:
        fname = "pbs_template.sh"
        shutil.copy2(os.path.join(template_dir, fname),
                     os.path.join(args.folder, fname))
    
    # Copy runner script
    shutil.copy2(os.path.join(script_dir, "runner.py"),
                 os.path.join(args.folder, "scripts", "runner.py"))

