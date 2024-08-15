import sys
import os


this_dir = os.path.dirname(__file__)

requirements = [
    os.path.join(this_dir, "evosdxl/requirements.txt"), 
    os.path.join(this_dir, "requirements.txt")
]


if __name__ == "__main__":
    os.system(f"{sys.executable} -m pip install --upgrade pip")
    for path in requirements:
        os.system(f"{sys.executable} -m pip install -r {path}")