"""
Global constants
Stores paths to directories used for input files, as well as constants referenced throughout the code base
"""
from pathlib import Path

from fastsim import vehicle
import os
# ./t3co
wkdir = Path(__file__).parent.parent

SWEEP_PATH = Path(os.path.abspath(__file__)).parents[1]/"sweep.py"

### modified from 1/2/3/4: conv/hev/phev/bev to match FASTSim strings

CONV = vehicle.CONV
HEV = vehicle.HEV
PHEV = vehicle.PHEV
BEV = vehicle.BEV
PT_TYPES_NUM_TO_STR = {CONV: "Conv", HEV: "HEV", PHEV: "PHEV", BEV: "BEV"}
###

FC_EFF_TYPES = {
    1: "SI",
    2: "Diesel - ISB280",
    3: "Diesel",
    4: "Fuel Cell",
    5: "Hybrid Diesel",
    6: "Diesel - HD",
    7: "Diesel - HDISM Scaled",
    8: "Diesel - HDISM Scaled",
    9: "CNG",
}
# note that FC_EFF_TYPES comes from fastsim and this here does not seem to override. Need to make sure it matches, or perhaps read it from fastsim.vehicle

STD_VAR_NAMES = "stdVarNames"

maxGvwrKg = 0
evGVWRAllowanceLbs = 0

# store reference to range cycle used for optimization
global_opt_range_cycle = None

# store scenario_name of current run
vocation_scenario = None

kwh_per_gge = 33.7

DieselGalPerGasGal = 0.887  # energy equivalent gallons of diesel per 1 gallon gas

kgH2_per_gge = 1.019  # https://epact.energy.gov/fuel-conversion-factors for Hydrogen

mps_to_mph = 2.23694  # 1 mps = 2.23694 mph
m_to_mi = 0.000621371  # 1 m = 0.000621371 mi


def get_kwh_per_gge():
    """
    This is a getter for kwh_per_gge, sim and scenario dependant var that can change
    important to get from one location each time so we can track when and how it's used

    Returns:
        kwh_per_gge (float): kWh per Gasoline Gallon Equivalent
    """
    return kwh_per_gge


# --------------------------- ###  directories and files ### ----------------------------


TCO_INTERMEDIATES = None
TCO_RESULTS = None
TCO_RES_FIGS = None

#  ## resources

# ./t3co/resources
OPTIMIZATION_AND_TCO_RCRS = Path(os.path.abspath(__file__)).parents[1] / "resources"

# ./t3co/resources/cycles
OPTIMIZATION_DRIVE_CYCLES = OPTIMIZATION_AND_TCO_RCRS / "cycles"

# benchmark resources
T2COBENCHMARKDATADIR = OPTIMIZATION_AND_TCO_RCRS / "benchmarkdata"

T3CO_INPUTS_DIR = OPTIMIZATION_AND_TCO_RCRS / "inputs"

def set_tco_intermediates():
    """
    This function sets path for TCO_INTERMEDIATES to save tsv files
    """
    global TCO_INTERMEDIATES

    # ./t3co/resources/f'vehicles/{vocation_scenario}/tco/tco_intermediates'
    TCO_INTERMEDIATES = (
        OPTIMIZATION_AND_TCO_RCRS
        / f"vehicles/{vocation_scenario}/tco/tco_intermediates"
    )
    if not TCO_INTERMEDIATES.exists():
        TCO_INTERMEDIATES.mkdir(parents=True)


def set_tco_results():
    """
    This function sets path for TCO_RESULTS
    """
    global TCO_RESULTS
    # ./t3co/resources/f'vehicles/{vocation_scenario}/tco/tco_results'
    TCO_RESULTS = (
        OPTIMIZATION_AND_TCO_RCRS / f"vehicles/{vocation_scenario}/tco/tco_results"
    )
    if not TCO_RESULTS.exists():
        TCO_RESULTS.mkdir(parents=True)

    global TCO_RES_FIGS
    # ./t3co/resources/f'vehicles/{vocation_scenario}/result_figures/'
    TCO_RES_FIGS = (
        OPTIMIZATION_AND_TCO_RCRS / f"vehicles/{vocation_scenario}/result_figures/"
    )
    if not TCO_RES_FIGS.exists():
        TCO_RES_FIGS.mkdir(parents=True)


OPTIMIZATION_RESOURCES_AUX = OPTIMIZATION_AND_TCO_RCRS / "auxiliary"
# FASTSim and Scenario input files
FASTSIM_INPUTS_FILE = "FASTSimInputsHeader.csv"
OTHER_INPUTS_FILE = "OtherInputs.csv"

# ./t3co/resources/"FASTSimInputs.csv"
FASTSIM_INPUTS = OPTIMIZATION_RESOURCES_AUX / FASTSIM_INPUTS_FILE

# ./t3co/resources/"OtherInputs.csv"
OTHER_INPUTS = OPTIMIZATION_RESOURCES_AUX / OTHER_INPUTS_FILE

# ./t3co/resources/'FuelPrices.csv'
REGIONAL_FUEL_PRICES_BY_TYPE_BY_YEAR = OPTIMIZATION_RESOURCES_AUX / "FuelPrices.csv"

RESIDUAL_VALUE_PER_YEAR = OPTIMIZATION_RESOURCES_AUX / "ResidualValues.csv"
MOO_KNOB_SWEEP_PLOTS_DIR = Path(os.path.abspath(__file__)).parents[1]/"tco_results" / "knob_sweep_results"

# TCO input files
write_files = False
ANN_TRAVEL_TSV = "annual-travel.tsv"
EMISSION_RATE_TSV = "emission-rate.tsv"
FUEL_EFF_TSV = "fuel-efficiency.tsv"
FUEL_EXPENSE_TSV = "fuel-expense.tsv"
FUEL_SPLIT_TSV = "fuel-split.tsv"
MARKET_SHARE_TSV = "market-share.tsv"
REGIONAL_SALES_TSV = "regional-sales.tsv"
SURVIVAL_TSV = "survival.tsv"
TRAVEL_EXP_TSV = "travel-expense.tsv"
VEH_EXP_TSV = "vehicle-expense.tsv"

# T3CO modules
TCO = "tests"

# Testing dirs

# ./t3co/tests
TESTSDIR = Path(os.path.abspath(__file__)).parents[1] / f"{TCO}/tco_tests"

# ./t3co/tests/tco_tests/'test_cycles'
TESTCYCLES = TESTSDIR / "test_cycles"

# ./t3co/tests/tco_tests/'test_vehicles'
TESTVEHICLES = TESTSDIR / "test_vehicles"

TESTVEHICLEINPUTS = TESTSDIR / "TCO_VEHICLE_TEST_INPUTS.csv"
TESTSCENARIOINPUTS = TESTSDIR / "TCO_SCENARIO_TEST_INPUTS.csv"

# ## useful functions

KG_2_LB = 2.20462


def kg_to_lbs(kgs):
    """
    This function converts kg to lb

    Args:
        kgs (float): mass in kg

    Returns:
        (float): mass in pounds
    """
    return kgs * KG_2_LB


def lbs_to_kgs(lbs):
    """
    This function converts lb to kg

    Args:
        lbs (float): mass in pounds

    Returns:
        (float): mass in kg
    """
    return lbs / KG_2_LB


def not_falsy(var):
    """
    This function returns True to verify that var is NOT falsy: not in [None, np.nan, 0, False]


    Args:
        var (float): variable to check

    Returns:
        (bool): True if not in [None, 0, False]
    """
    return var not in [None, 0, False]
