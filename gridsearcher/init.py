import os
import shutil
import sys


def init(args):
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
    module_dir, _ = os.path.split(__file__)
    root_dir, _ = os.path.split(module_dir)
    script_dir = os.path.join(root_dir, "scripts")
    template_dir = os.path.join(root_dir, "templates")

    if args.xgb:
        fname = "xgb_grid.json"
        shutil.copy2(os.path.join(template_dir, fname),
                     os.path.join(args.folder, fname))
    
    if args.pbs:
        for fname in ["pbs_train.sh", "pbs_eval.sh"]:
            shutil.copy2(os.path.join(template_dir, fname),
                        os.path.join(args.folder, fname))
    
    # Copy runner script
    shutil.copy2(os.path.join(script_dir, "train.py"),
                 os.path.join(args.folder, "scripts", "train.py"))
    
    # Copy evaluate script
    shutil.copy2(os.path.join(script_dir, "evaluate.py"),
                 os.path.join(args.folder, "scripts", "evaluate.py"))

