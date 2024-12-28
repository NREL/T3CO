# %%
from __future__ import annotations

import ast
import os
import warnings
from math import ceil
from pathlib import Path

import fastsim
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

from t3co.run import Global as gl
from t3co.run import run_scenario


class OpportunityCost:
    payload_cap_cost_multiplier: float = 0
    

    def __init__(self):
        pass

# %%
# if __name__ == "__main__":
#     oc = main()
