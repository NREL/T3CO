# %%
import json
import time
from pathlib import Path

import yaml
import t3co
import pandas as pd
import os

from t3co.tco import ledger
from t3co.input_data import vehicle, scenario, config
from t3co.energy_models import energy
from t3co.tco.tcocalc import TCOCalc

start = time.time()
input_vehicle = vehicle.Vehicle().from_db(selection=1, vehicle_db_file=Path(__file__).parents[1]/"t3co"/"resources"/"inputs"/"Demo_FY22_vehicle_model_assumptions.csv")
input_vehicle.set_veh_kg()
input_scenario = scenario.Scenario().from_db(selection=1, scenario_file=Path(__file__).parents[1]/"t3co"/"resources"/"inputs"/"Demo_FY22_scenario_assumptions.csv")
input_energy = energy.Energy('exogenous', mpgge=4.0, primary_fuel_range_mi=200.0)

tco_0 = TCOCalc(1, input_vehicle, input_scenario, input_energy)
# print(tco_0)

#%%
output_ledger =  ledger.Ledger(vehicle=input_vehicle, scenario=input_scenario, energy=input_energy)
filepath="../results/save_dict.json"
output_ledger.to_dict(filepath, flatten=False)

#%%
# results_dict = output_ledger.to_dict( flatten=True)
# with open(filepath, 'w') as f:
#     json.dump(handle_nan(results_dict), f)

# %%
print(f'T3CO Run time: {time.time()-start}')

if __name__=='__main__':
    pass