# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import time
import numpy as np
import matplotlib.pyplot as plt

from dataclasses import asdict
import pandas as pd
import importlib


from t3co import Global as gl
from t3co import moo
importlib.reload(moo)


# %%
RANGE, ACCEL, GRADE, TCO = moo.RANGE, moo.ACCEL, moo.GRADE, moo.TCO


# optimization scenario parameters where we get our baseline vehicle and scenario
# eventually needs parameterization
vnum = 1  #
vocation = "Conv 2020 tech,  750 mi range"
gl.vocation_scenario = vocation
gl.FASTSIM_INPUTS = gl.T2COBENCHMARKDATADIR / 't3cobenchmarkFASTSimInputs.csv'
gl.OTHER_INPUTS = gl.T2COBENCHMARKDATADIR / 't3cobenchmarkOtherInputs.csv'

# can adjust this if we don't get good benchmark/viable results

# sol not found
pop_size = 10
n_max_gen = 15
tol = 0.01

# possible HEV knobs
# light-weighting, fuel converter size, engine efficiency, CdA percent, battery and motor size
knobs_bounds_all = {
    'CdA_perc_imp': (5.0, 25.0),
    'fc_max_kw': (200, 500),  # fc_max_kw could be used for optimization of HEV
    'ess_max_kwh': (1, 300),
    'mc_max_kw': (10, 300),
    'fc_peak_eff': (46, 60),
    'wt_delta_perc': (0, 25),
}


# %%

for knob, bounds in knobs_bounds_all.items():
    problem = moo.run_optimization(
        pop_size, n_max_gen, tol, {knob: bounds}, vnum, 
        obj_list=[TCO], use_jit=True, optimize_pt=gl.HEV, 
        skip_optimization=True
    )
    xs = np.linspace(bounds[0], bounds[1], 15)

    ys = []

    for x in xs:
        ys.append(problem.get_objs([x]))

    ys = np.array(ys)

    plt.figure()
    plt.plot(xs, ys)
    plt.xlabel(knob)
    plt.ylabel('TCO [$]')