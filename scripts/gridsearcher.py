import argparse

from init import init
from build import build
from submit import submit


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="Subcommands")

    # Init subparser
    subparser_init = subparsers.add_parser("init",
        help="Initialize project directory")
    # Init args
    subparser_init.add_argument("folder",
        help="Name of grid-search folder")
    subparser_init.add_argument("-xgb", action="store_true",
        help="Copy XGBoost templates")
    subparser_init.add_argument("-pbs", action="store_true",
        help="Copy PBS templates")
    subparser_init.set_defaults(func=init)
    
    # Build subparser
    subparser_build = subparsers.add_parser("build",
        help="Build models from configuration file")
    # Build args
    subparser_build.add_argument("config",
        help="Grid-search configuration file")
    subparser_build.set_defaults(func=build)
    
    # Submit subparser
    subparser_submit = subparsers.add_parser("submit",
        help="Submit to cluster")
    # Submit args
    subparser_submit.add_argument("-n", type=int,
        help="Number of jobs to submit")
    subparser_submit.add_argument("script",
        help="Path to PBS script")
    subparser_submit.set_defaults(func=submit)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    args.func(args)
