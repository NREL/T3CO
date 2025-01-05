"""
Global constants
Stores paths to directories used for input files, as well as constants referenced throughout the code base
"""

from pathlib import Path

from fastsim import vehicle
import os

# ./t3co
wkdir = Path(__file__).parent.parent

SWEEP_PATH = Path(__file__).resolve().parents[1] /"cli"/ "sweep.py"

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


maxGvwrKg = 0
evGVWRAllowanceLbs = 0

# store reference to range cycle used for optimization
global_opt_range_cycle = None

# store scenario_name of current run
vocation_scenario = None

KWH_PER_GGE = 33.7

DieselGalPerGasGal = 0.887  # energy equivalent gallons of diesel per 1 gallon gas

kgH2_per_gge = 1.019  # https://epact.energy.gov/fuel-conversion-factors for Hydrogen

mps_to_mph = 2.23694  # 1 mps = 2.23694 mph
m_to_mi = 0.000621371  # 1 m = 0.000621371 mi

diesel_to_gge = 1 * (33.7 / 37.95)


# --------------------------- ###  directories and files ### ----------------------------


TCO_INTERMEDIATES = None
TCO_RESULTS = None
TCO_RES_FIGS = None

#  ## resources

# ./t3co/resources
RESOURCES_FOLDERPATH = Path(__file__).parents[1].resolve() / "resources"
# ./t3co/resources/cycles
OPTIMIZATION_DRIVE_CYCLES = RESOURCES_FOLDERPATH / "cycles"

# benchmark resources
T2COBENCHMARKDATADIR = RESOURCES_FOLDERPATH / "benchmarkdata"

T3CO_INPUTS_DIR = RESOURCES_FOLDERPATH / "inputs"


def set_tco_intermediates():
    """
    This function sets path for TCO_INTERMEDIATES to save tsv files
    """
    global TCO_INTERMEDIATES

    # ./t3co/resources/f'vehicles/{vocation_scenario}/tco/tco_intermediates'
    TCO_INTERMEDIATES = (
        RESOURCES_FOLDERPATH
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
        RESOURCES_FOLDERPATH / f"vehicles/{vocation_scenario}/tco/tco_results"
    )
    if not TCO_RESULTS.exists():
        TCO_RESULTS.mkdir(parents=True)

    global TCO_RES_FIGS
    # ./t3co/resources/f'vehicles/{vocation_scenario}/result_figures/'
    TCO_RES_FIGS = (
        RESOURCES_FOLDERPATH / f"vehicles/{vocation_scenario}/result_figures/"
    )
    if not TCO_RES_FIGS.exists():
        TCO_RES_FIGS.mkdir(parents=True)


OPTIMIZATION_RESOURCES_AUX = RESOURCES_FOLDERPATH / "auxiliary"
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
MOO_KNOB_SWEEP_PLOTS_DIR = (
    Path(os.path.abspath(__file__)).parents[1] / "tco_results" / "knob_sweep_results"
)

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


def kg_to_lbs(kgs: float) -> float:
    """
    This function converts kg to lb

    Args:
        kgs (float): mass in kg

    Returns:
        (float): mass in pounds
    """
    return kgs * KG_2_LB


def lbs_to_kgs(lbs: float) -> float:
    """
    This function converts lb to kg

    Args:
        lbs (float): mass in pounds

    Returns:
        (float): mass in kg
    """
    return lbs / KG_2_LB


def not_falsy(var: float) -> bool:
    """
    This function returns True to verify that var is NOT falsy: not in [None, np.nan, 0, False]


    Args:
        var (float): variable to check

    Returns:
        (bool): True if not in [None, 0, False]
    """
    return var not in [None, 0, False]
