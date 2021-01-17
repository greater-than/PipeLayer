import sys
from pathlib import Path

project_root = Path(__file__).parents[1]
sys.path.insert(0, f"{project_root}/src")
sys.path.insert(1, f"{project_root}/examples")
sys.path.insert(2, f"{project_root}/test")
