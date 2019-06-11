"""
Constants that are used by many modules
"""
import os
from pathlib import Path

bayesbench_dir = Path(__file__).parent.parent

parent_dir = bayesbench_dir.parent
posterior_db_location = os.path.join(parent_dir, "posterior_db")

output_dir = os.path.join(bayesbench_dir, "experiments_out")
