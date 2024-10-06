# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import seaborn as sns

sns.set()

import importlib
from t3co.tco import opportunity_cost as oppcost
importlib.reload(oppcost)


# %%
free_dwells = np.linspace(0, 1.5, 15)
wt_xEV_diffs = np.linspace(-5, 5, 100) * 1_000

oc = oppcost.OpportunityCost()
oc.free_dwell_time_hr = 1

oppcosts = np.array([[{}] * len(wt_xEV_diffs)] * len(free_dwells))
for j, wt_xEV_diff in enumerate(wt_xEV_diffs):
    print(f'\nOuter iteration {j:d}')
    print(f'wt_xEV_Diff = {wt_xEV_diff:.0f} lbs')
    for i, free_dwell in enumerate(free_dwells):
        print(f'Inner iteration {i:d}')
        print(f'free_dwell = {free_dwell:.2f} hrs')
        oc.free_dwell_time_hr = free_dwell
        oc.wt_xEVempty_lb = oc.wt_base_vehicle_lb + wt_xEV_diff
        oppcosts[i, j] = oc.set_opp_cost()


# %%
tot_opp_cost_xy = np.array([[oppcosts[i][j]['tot_opp_cost_per_mi']
                    for i in range(len(free_dwells))] 
                   for j in range(len(wt_xEV_diffs))])

labor_cost_xy = np.array([[oppcosts[i][j]['labor_cost_per_mi']
                    for i in range(len(free_dwells))] 
                   for j in range(len(wt_xEV_diffs))])

payload_cost_xy = np.array([[oppcosts[i][j]['payload_cost_per_mi']
                    for i in range(len(free_dwells))] 
                   for j in range(len(wt_xEV_diffs))])

conv_payload_rev_xy = np.array([[oppcosts[i][j]['CV_rev__mi']
                    for i in range(len(free_dwells))] 
                   for j in range(len(wt_xEV_diffs))])

# conv_payload_rev_xy = np.array([[oppcosts[i][j]['xEV_rev__mi']
#                     for i in range(len(free_dwells))] 
#                    for j in range(len(wt_xEV_diffs))])

time_cost_xy = np.array([[oppcosts[i][j]['time_cost_per_mi']
                    for i in range(len(free_dwells))] 
                   for j in range(len(wt_xEV_diffs))])

payload_time_factor_xy = np.array([[oppcosts[i][j]['payload_time_factor']
                    for i in range(len(free_dwells))] 
                   for j in range(len(wt_xEV_diffs))])

net_dwell_time_xy = np.array([[oppcosts[i][j]['net_fueling_dwell_time_hr_per_yr']
                    for i in range(len(free_dwells))] 
                   for j in range(len(wt_xEV_diffs))])

dwell_time_xy = np.array([[oppcosts[i][j]['dwell_time_hr']
                    for i in range(len(free_dwells))] 
                   for j in range(len(wt_xEV_diffs))])


# %%
plt.plot(oc.weight_x_lb, oc.CV_cargo_kde, label='conventional')
plt.xlabel('Cargo Weight [lb]')
plt.ylabel('Probability Density')
plt.title('Cargo Weight Probability Density')
plt.legend()

# %% [markdown]
# ## Parametric plots

# %%
for i in range(len(free_dwells)):
    if (i % 4 == 0) or i == len(free_dwells) - 1:
        plt.plot(wt_xEV_diffs, tot_opp_cost_xy[:,i], 
                 label='{:.2f}'.format(free_dwells[i]))
    else:
        plt.plot(wt_xEV_diffs, tot_opp_cost_xy[:,i], linestyle='--')
plt.xlabel('xEV Wt. Minus CV Wt. [lb]')
plt.ylabel('Total Opportunity Cost [$/mi]')
plt.title('Total Opportunity Cost')
plt.legend(title='Free Dwell Time [hr]')


# %%
for i in range(len(free_dwells)):
    if (i % 4 == 0) or i == len(free_dwells) - 1:
        plt.plot(wt_xEV_diffs, (tot_opp_cost_xy / conv_payload_rev_xy)[:,i], 
                 label='{:.2f}'.format(free_dwells[i]))
    else:
        plt.plot(wt_xEV_diffs, (tot_opp_cost_xy / conv_payload_rev_xy)[:,i], linestyle='--')
plt.xlabel('xEV Wt. Minus CV Wt. [lb]')
plt.ylabel('Cost Ratio')
plt.title('Total Opportunity Cost\nPer Conventional Revenue')
plt.legend(title='Free Dwell Time [hr]')


# %%
# for i in range(len(free_dwells)):
#     if (i % 4 == 0) or i == len(free_dwells) - 1:
#         plt.plot(wt_xEV_diffs, payload_cost_xy[:,i], 
#                  label='{:.2f}'.format(free_dwells[i]))
#     else:
#         plt.plot(wt_xEV_diffs, payload_cost_xy[:,i], linestyle='--')
# plt.legend(title='Free Dwell Time [hr]')
plt.plot(wt_xEV_diffs, payload_cost_xy[:, 0])
plt.xlabel('xEV Wt. Minus CV Wt. [lb]')
plt.ylabel('Payload Cost [$/mi]')
plt.title('Payload Cost')


# %%
for i in range(len(free_dwells)):
    if (i % 4 == 0) or i == len(free_dwells) - 1:
        plt.plot(wt_xEV_diffs, time_cost_xy[:,i], 
                 label='{:.2f}'.format(free_dwells[i]))
    else:
        plt.plot(wt_xEV_diffs, time_cost_xy[:,i], linestyle='--')
plt.xlabel('xEV Wt. Minus CV Wt. [lb]')
plt.ylabel('Time Cost [$/mi]')
plt.title('Time Cost')
plt.legend(title='Free Dwell Time [hr]')

# %% [markdown]
# ## Contour plots

# %%
x2d, y2d = np.meshgrid(free_dwells, wt_xEV_diffs / 1000)


# %%
FCS = plt.contourf(x2d, y2d, tot_opp_cost_xy / conv_payload_rev_xy * 100, 20, cmap='jet')
plt.xlabel('Free Dwell Time (hr)')
plt.ylabel('xEV Wt. Minus CV Wt. (1000 lb)')
cb = plt.colorbar(FCS)
cb.set_label('%')
plt.title('Total Opportunity Cost\nPer Conventional Revenue')
plt.show()


# %%
FCS = plt.contourf(x2d, y2d, tot_opp_cost_xy, 20, cmap='jet')
plt.xlabel('Free Dwell Time (hr)')
plt.ylabel('xEV Wt. Minus CV Wt. (1000 lb)')
cb = plt.colorbar(FCS)
cb.set_label('$/Mile')
plt.title('Total Opportunity Cost Per Mile')
plt.show()


# %%
FCS = plt.contourf(x2d, y2d, payload_cost_xy, 15, cmap='jet')
plt.xlabel('Free Dwell Time (hr)')
plt.ylabel('xEV Wt. Minus CV Wt. (1000 lb)')
cb = plt.colorbar(FCS)
cb.set_label("$/Mile")
plt.title('Payload Cost Per Mile')
plt.show()


# %%
FCS = plt.contourf(x2d, y2d, time_cost_xy, 15, cmap='jet')
plt.xlabel('Free Dwell Time (hr)')
plt.ylabel('xEV Wt. Minus CV Wt. (1000 lb)')
cb = plt.colorbar(FCS)
cb.set_label("$/Mile")
plt.title('Time Cost Per Mile')
plt.show()


# %%
FCS = plt.contourf(x2d, y2d, labor_cost_xy, 15, cmap='jet')
plt.xlabel('Free Dwell Time (hr)')
plt.ylabel('xEV Wt. Minus CV Wt. (1000 lb)')
cb = plt.colorbar(FCS)
cb.set_label("$/Mile")
plt.title('Labor Cost Per Mile')
plt.show()


# %%
FCS = plt.contourf(x2d, y2d, payload_time_factor_xy, 15, cmap='jet')
plt.xlabel('Free Dwell Time (hr)')
plt.ylabel('xEV Wt. Minus CV Wt. (1000 lb)')
plt.title('Payload Time Factor')
plt.colorbar(FCS)
plt.show()


