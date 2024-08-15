import sys
import os

from argparse import ArgumentParser, Namespace


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--preinstall_model", action="store_true")
    return parser.parse_args()


this_dir = os.path.dirname(__file__)

requirements = [
    os.path.join(this_dir, "evosdxl/requirements.txt"), 
    os.path.join(this_dir, "requirements.txt")
]


if __name__ == "__main__":
    args = parse_arguments()
    os.system(f"{sys.executable} -m pip install --upgrade pip")
    for path in requirements:
        os.system(f"{sys.executable} -m pip install -r {path}")
    if args.preinstall_model:
        from evosdxl.evosdxl_jp_v1 import load_evosdxl_jp
        load_evosdxl_jp("cpu")