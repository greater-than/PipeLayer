# This module can be deleted if running this app outside of the pipelayer project
import os
import sys
from pathlib import Path

project_root = Path(os.path.abspath(__file__)).parents[3]
sys.path.insert(0, f"{project_root}/src")
