# %%
from pathlib import Path
import t3co
import pandas as pd
import os

from t3co.tco import ledger
from t3co.input_data import vehicle, scenario, config
from t3co.energy_models import energy
from t3co.tco.tcocalc import TCOCalc

input_vehicle = vehicle.Vehicle().from_db(selection=1, vehicle_db_file=Path(__file__).parents[1]/"t3co"/"resources"/"inputs"/"Demo_FY22_vehicle_model_assumptions.csv")
input_vehicle.set_veh_kg()
input_scenario = scenario.Scenario().from_db(selection=1, scenario_file=Path(__file__).parents[1]/"t3co"/"resources"/"inputs"/"Demo_FY22_scenario_assumptions.csv")
input_energy = energy.Energy('exogenous', mpgge=4.0, primary_fuel_range_mi=200.0)

tco_0 = TCOCalc(1, input_vehicle, input_scenario, input_energy)
print(tco_0)
# %%
if __name__=='__main__':
    pass