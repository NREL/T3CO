"""Module containing functions for calculating fuel economy objectives."""
# %%
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import fastsim
import matplotlib.pyplot as plt
import numpy as np

from t3co.run import Global as gl
from t3co.run import run_scenario


def get_range_mi(mpgge_info:dict, vehicle:fastsim.vehicle.Vehicle, scenario) -> dict:
    """
    This funcion computes range [miles] from mpgge using vehicle powertrain type and energy (or fuel) store size.

    Considerations:
    - at some point each vehicle powertrain type could employ the concept 
    of a "first fuel" or "primary fuel" - so return a primary fuel-based range for all 
    powertrains.  
    - PHEVs have two fuels (generally diesel and electricity). So return two ranges:
    -- One for determining range during optimization
        i.e. the CD range that PHEVs are commonly specified with 
        (e.g. PHEV-50 = PHEV with 50 mi AER "All-Electric Range" ~= CD range)
    -- One that represents the "true" total PHEV range (CD + CS using both ESS and FS)

    Args:
        mpgge_info (dict): Dictionary containing MPGGE breakdown 
        vehicle (fastsim.vehicle.Vehicle): FASTSim vehicle object of analysis vehicle
        scenario (run_scenario.Scenario): Scenario object of current selection

    Returns:
        range_dict (dict): Dictionary containing different range results
    """
    range_dict = {}
    kwh_per_gge = gl.get_kwh_per_gge()
    if vehicle.veh_pt_type == gl.BEV:
        assert vehicle.fs_kwh == 0 and vehicle.fc_max_kw == 0, "Error! BEV vehicle has non-zero ICE attributes - vehicle mass calculation may be off"
        mpgge = mpgge_info["mpgge"]  # use fuel efficiency from battery
        range_mi = vehicle.ess_max_kwh * (vehicle.max_soc - vehicle.min_soc) * mpgge / kwh_per_gge
        range_dict['primary_fuel_range_mi'] = range_mi
    elif vehicle.veh_pt_type == gl.CONV:
        assert vehicle.ess_max_kwh == 0 and vehicle.mc_max_kw == 0, "Error! CONV vehicle has non-zero BEV attributes - vehicle mass calculation may be off"
        mpgge = mpgge_info["mpgge"]
        range_mi = (vehicle.fs_kwh / kwh_per_gge) * mpgge
        range_dict['primary_fuel_range_mi'] = range_mi
    elif vehicle.veh_pt_type == gl.HEV:
        mpgge = mpgge_info["mpgge"]
        elec_range_mi = vehicle.ess_max_kwh * (vehicle.max_soc - vehicle.min_soc) * mpgge / kwh_per_gge
        conv_range_mi = (vehicle.fs_kwh / kwh_per_gge) * mpgge
        range_mi = elec_range_mi + conv_range_mi
        range_dict['primary_fuel_range_mi'] = range_mi
    elif vehicle.veh_pt_type == gl.PHEV:
        # https://github.nrel.gov/AVCI/FASTSim_TCO_Truck/issues/24#issuecomment-39958
        # charge depleting range [miles]
        # CDrangeMiles = MIN( ESSmaxKWh*(CDmaxSOC- CDminSOC)/ CDelectricityKWhperMile , maxFuelStorKWh/33.7/ CDfuelGGEperMile )
        cd_range_mi = min(
            vehicle.ess_max_kwh * (vehicle.max_soc - vehicle.min_soc) / mpgge_info['cd_electric_kwh__mi'],
            vehicle.fs_kwh / kwh_per_gge * mpgge_info['cd_fuel_mpgge']
        )
        # charge sustaining range [miles]
        # note, CS range in this way of thinking, is essentially what range is *left over* after you've exhausted the battery to min SOC 
        # and switch into CS mode from CD mode, thus we subtract cd_gge_used from the GGE fuel stores of the vehicle
        cd_gge_used = cd_range_mi / mpgge_info['cd_fuel_mpgge']
        gge_capacity = vehicle.fs_kwh / kwh_per_gge
        cs_range_mi = (gge_capacity - cd_gge_used) * mpgge_info['cs_fuel_mpgge']
        true_range_mi = cd_range_mi + cs_range_mi
        range_dict= {
            "cd_aer_phev_range_mi": cd_range_mi,
            "cs_phev_range_mi" : cs_range_mi,
            "true_phev_range_mi": true_range_mi,
            "primary_fuel_range_mi": cd_range_mi,
            }
    # if sim_drive:
    #     range_dict["cycle_distance_mi"] = sum(sim_drive.cyc.mps * np.diff(sim_drive.cyc.time_s)[0]) * gl.m_to_mi
    #     range_dict["mean_cyc_speed_mph"] = sum(sim_drive.cyc.mps)/max(sim_drive.cyc.time_s) * gl.mps_to_mph 
    # elif range_cyc:
    #     range_dict["cycle_distance_mi"] = sum(range_cyc.mps * np.diff(range_cyc.time_s)[0]) * gl.m_to_mi
    #     range_dict["mean_cyc_speed_mph"] = sum(range_cyc.mps)/max(range_cyc.time_s) * gl.mps_to_mph 
    return range_dict


def get_sim_drive(erc, v, scenario):
    """
    This helper method returns a FASTSim SimDrive object using the vehicle, drive cycle and scenario

    Args:
        erc (fastsim.cycle.Cycle| List[Tuple[fastsim.cycle.Cycle, float): FASTSim range cycle object or list of tuples of cycles
        v (fastsim.vehicle.Vehicle): FASTSim vehicle object for analysis vehicle
        scenario (run_scenario.Scenario): Scenario object for current selection

    Returns:
        sim_drive (fastsim.simdrive.SimDrive): FASTSim SimDrive object
    """
    sim_drive = fastsim.simdrive.SimDrive(erc, v)
    sim_drive = sim_drive.to_rust()
    
    sim_params = sim_drive.sim_params
    sim_params.reset_orphaned()
    # sim_params.verbose = False
    if scenario.missed_trace_correction:
        sim_params.missed_trace_correction = True
        sim_params.max_time_dilation = scenario.max_time_dilation
        sim_params.min_time_dilation = scenario.min_time_dilation
        sim_params.time_dilation_tol = scenario.time_dilation_tol
    sim_drive.sim_params = sim_params

    props = sim_drive.props
    props.reset_orphaned()  # see if this is needed
    props.kwh_per_gge = gl.get_kwh_per_gge()
    sim_drive.props = props

    return sim_drive

def get_mpgge(eff_range_cyc:fastsim.cycle.Cycle | List[Tuple[fastsim.cycle.Cycle, float]],
               v:fastsim.vehicle.Vehicle, scenario, diagnostic=False):
    """
    This helper method gets the composite mpgge fuel efficiency of vehicle for each efficiency_range Drive Cycle and weight.
    It runs the vehicle using efficiency range cycle(s) and returns mpgge based on the powertrain type

    Method computes a composite mpgge from multiple drive cycles and weights for each cycle.
    If the user passes in a single Drive Cycle rather than a list of tuples, the base case of
    a composite mpgge from a single Drive Cycle and a single weight, 1, is computed.

    Also updates the vehicle's corresponding scenario object

    Args:
        eff_range_cyc (fastsim.cycle.Cycle | List[Tuple[fastsim.cycle.Cycle, float]]): efficiency range cycle
        v (fastsim.vehicle.Vehicle): FASTSim vehicle object for analysis vehicle
        scenario (run_scenario.Scenario): Scenario object for current selection
        diagnostic (bool, optional): if True, returns all mpgge dicts. Defaults to False.

    Raises:
        ValueError: unknown vehicle powertrain type

    Returns:
        mpgge_comp (dict): Dictionary containing MPGGE breakdowns
        sim_drives (List[fastsim.simdrive.SimDrive]): List of simdrives for charge depleting and charge sustaining cycles
        mpgges (List[dict], optional): if diagnostic==True, returns additional 
        
    """

    if not isinstance(eff_range_cyc, list):
        eff_range_cyc = [(eff_range_cyc, 1)]

    if v.veh_pt_type == gl.BEV:
        assert v.mc_max_kw > 0, "motor size is 0 kw in BEV - will lead to faulty results"
        assert v.fs_kwh == 0 and v.fc_max_kw == 0, "Error! BEV vehicle has non-zero ICE attributes - vehicle mass calculation may be off"
    elif v.veh_pt_type == gl.CONV:
        assert v.fc_max_kw > 0, "engine size is 0 kw in CONV - will lead to faulty results"
        assert v.ess_max_kwh == 0 and v.mc_max_kw == 0, "Error! CONV vehicle has non-zero BEV attributes - vehicle mass calculation may be off"
    elif v.veh_pt_type == gl.PHEV:
        assert v.fc_max_kw > 0, "engine size is 0 kw in CONV - will lead to faulty results"
        assert v.mc_max_kw > 0, "motor size is 0 kw in BEV - will lead to faulty results"
    elif v.veh_pt_type == gl.HEV:
        pass
    else:
        raise ValueError(f"unknown vehicle powertrain type {v.veh_pt_type}")

    mpgges = []
    weights = []
    sim_drives = []
    for cycle_weight in eff_range_cyc:
        # efficiency-range cycle, weight 
        erc, w = cycle_weight    

        if v.veh_pt_type == gl.PHEV:
            # get two copies of cycle, rename
            cd_erc = erc.copy()
            cs_erc = erc.copy()
            cd_erc.name = 'CD_' + erc.name 
            
            #
            # Charge Depleting Cycle first
            #
            ess_max_kwh_orig = v.ess_max_kwh
            ess_max_kw_orig  = v.ess_max_kw
            veh_kg_orig      = v.veh_kg
            # infinite battery hack (with no extra weight) to simulate charge depleting behavior
            v.veh_override_kg = veh_kg_orig
            run_scenario.set_max_battery_kwh(v, 50e3) 
            run_scenario.set_max_battery_power_kw(v, 1000)
            # don't want extra weight from huge battery
            sim_drive_cd = get_sim_drive(cd_erc, v, scenario)
            assert sim_drive_cd.veh.veh_kg == veh_kg_orig, f'sim_drive.veh.veh_kg == veh_kg_orig / {round(sim_drive_cd.veh.veh_kg)} == {round(veh_kg_orig)}' 
            assert sim_drive_cd.veh.ess_max_kwh == v.ess_max_kwh, f'sim_drive.veh.ess_max_kwh == v.ess_max_kwh / {round(sim_drive_cd.veh.ess_max_kwh)} == {round(v.ess_max_kwh)}' 
            sim_drive_cd.sim_drive(init_soc=v.max_soc)
            v.veh_override_kg = None
            
            #
            # Charge Sustaining Cycle second
            #
            # reset battery to inputs for charge sustaining behavior
            run_scenario.set_max_battery_kwh(v, ess_max_kwh_orig) 
            run_scenario.set_max_battery_power_kw(v, ess_max_kw_orig)          
            # we're supposed to run this as a "hybrid" so set 
            # veh_pt_type to gl.HEV so that FASTSim does SOC balancing, run as an HEV, basically
            v.veh_pt_type = gl.HEV
            sim_drive_cs = get_sim_drive(cs_erc, v, scenario)
            sim_drive_cs.sim_drive()


            # CS calcs
            assert sim_drive_cs.props.kwh_per_gge == gl.get_kwh_per_gge(), "fuel LHV not consistent between T3CO and FASTSim"
            cs_fuel_kwh_out_ach = np.sum(sim_drive_cs.fs_kwh_out_ach) 
            cs_fuel_kwh__mi = cs_fuel_kwh_out_ach / np.sum(sim_drive_cs.dist_mi)

            # CD calcs
            # sim_drive_cd.fs_kwh_out_ach[i] = sim_drive_cd.fs_kw_out_ach[i] * sim_drive_cd.cyc.dt_s[i] * (1 / 3.6e3)
            assert sim_drive_cd.props.kwh_per_gge == gl.get_kwh_per_gge(), "fuel LHV not consistent between T3CO and FASTSim"
            cd_fuel_kwh_out_ach = np.sum(sim_drive_cd.fs_kwh_out_ach) 
            cd_elec_kwh_out_ach = np.sum(np.array(sim_drive_cd.ess_kw_out_ach) * np.array(sim_drive_cd.cyc.dt_s) / 3.6e3)
            cd_elec_mpgge  = np.sum(sim_drive_cd.dist_mi) / (cd_elec_kwh_out_ach / gl.get_kwh_per_gge())
            cd_electric_kwh__mi = cd_elec_kwh_out_ach / np.sum(sim_drive_cd.dist_mi)
            cd_fuel_kwh__mi = cd_fuel_kwh_out_ach / np.sum(sim_drive_cd.dist_mi)
            
            v.veh_pt_type = gl.PHEV
            v.set_derived()
            assert v.veh_kg == veh_kg_orig
            assert v.ess_max_kwh == ess_max_kwh_orig
            assert v.ess_max_kw == ess_max_kw_orig
            assert v.veh_pt_type == gl.PHEV

            # TODO: some CS sd's have sum(fs_kwh_out_ach) == 0 ... how?
            # These are probably bad designs and should be skipped

            # TODO: these kinds of outputs could be turned into a dataclass to set
            # desired outputs and have stricter checks
            mpgge = {
                #### Charge depleting ####
                'cd_electric_mpgge': cd_elec_mpgge,
                'cd_grid_electric_mpgge': cd_elec_mpgge * v.chg_eff,      # can be used for TCO CD mpgge electric
                'cd_fuel_mpgge': sim_drive_cd.mpgge,                
                'cd_fuel_mpgde': sim_drive_cd.mpgge / gl.DieselGalPerGasGal,                
                "cd_electric_kwh__mi": cd_electric_kwh__mi,
                "cd_fuel_kwh__mi": cd_fuel_kwh__mi,
                'cd_fuel_used_kwh': cd_fuel_kwh_out_ach,
                'cd_elec_used_kwh': cd_elec_kwh_out_ach,

                #### Charge sustaining ####
                "cs_fuel_mpgge": sim_drive_cs.mpgge,
                "cs_fuel_mpgde": sim_drive_cs.mpgge / gl.DieselGalPerGasGal,
                "cs_fuel_kwh__mi": cs_fuel_kwh__mi,
            }
            sim_drives.append(sim_drive_cd)
            sim_drives.append(sim_drive_cs)
        else:
            sim_drive = get_sim_drive(erc, v, scenario)
            sim_drive.sim_drive()

            # FASTSim BEV and PHEV have two different fuel efficiencies, the mpgge from battery and the mpgge from grid
            # grid_mpgge is really just mpgge multiplied by the charger efficiency fraction
            # grid_mpgge is used for fuel cost calculations
            # TCO fuel cost = vmt / mpgge * $/gge
            # for CONV and HEV
            # this is on an energy basis (mpgge has no electric component if the vehicle is CONV)
            # if vehicle is HEV mpgge = mpgge_from_fs_kwh_used + mpgge_from_battery_kwh_used
            if v.veh_pt_type in [gl.CONV, gl.HEV]:
                mpgge_both = sim_drive.mpgge
            else:
                mpgge_both = sim_drive.mpgge + (1/sim_drive.electric_kwh_per_mi) * gl.get_kwh_per_gge()
            mpgge = {
                # combine ICE and electric PT components for overall mpgge
                "mpgge": mpgge_both,
                "grid_mpgge": mpgge_both * sim_drive.veh.chg_eff, 
                "mpgde": mpgge_both / gl.DieselGalPerGasGal,
                # TODO, have this checked
                "kwh_per_mi": (sum(sim_drive.fs_kwh_out_ach) + ((sim_drive.roadway_chg_kj + sim_drive.ess_dischg_kj) / 3.6e3)) / sum(sim_drive.dist_mi),  
            }
            sim_drives.append(sim_drive)

        mpgges.append(mpgge)
        weights.append(w)

    if v.veh_pt_type == gl.PHEV:
        cs_fuel_mpgge_i = np.array([m['cs_fuel_mpgge'] for m in mpgges])
        cs_fuel_mpgde_i = np.array([m['cs_fuel_mpgde'] for m in mpgges])
        cs_fuel_kwh__mi_i = np.array([m['cs_fuel_kwh__mi'] for m in mpgges])

        cd_fuel_used_kwh_i = [m['cd_fuel_used_kwh'] for m in mpgges]
        cd_battery_used_kwh_i = [m['cd_elec_used_kwh'] for m in mpgges]
        cd_fuel_mpgge_i = np.array([m['cd_fuel_mpgge'] for m in mpgges])
        cd_fuel_mpgde_i = np.array([m['cd_fuel_mpgde'] for m in mpgges])
        cd_electric_mpgge_i = np.array([m['cd_electric_mpgge'] for m in mpgges])
        cd_grid_electric_mpgge_i = np.array([m['cd_grid_electric_mpgge'] for m in mpgges])
        cd_electric_kwh__mi_i = np.array([m['cd_electric_kwh__mi'] for m in mpgges])
        cd_fuel_kwh__mi_i = np.array([m['cd_fuel_kwh__mi'] for m in mpgges])
              
        mpgge_comp = {
            # Charge sustaining
            'cs_fuel_mpgge': np.sum(weights) / np.sum(np.divide(weights, cs_fuel_mpgge_i, out=np.zeros_like(cs_fuel_mpgge_i), where=cs_fuel_mpgge_i!=0, casting='unsafe')),
            'cs_fuel_mpgde': np.sum(weights) / np.sum(np.divide(weights, cs_fuel_mpgde_i, out=np.zeros_like(cs_fuel_mpgde_i), where=cs_fuel_mpgde_i!=0, casting='unsafe')),
            'cs_fuel_kwh__mi': np.sum(weights) / np.sum(np.divide(weights, cs_fuel_kwh__mi_i, out=np.zeros_like(cs_fuel_kwh__mi_i), where=cs_fuel_kwh__mi_i!=0, casting='unsafe')),

            # Charge depleting
            'cd_fuel_used_kwh_total': sum(cd_fuel_used_kwh_i),
            'cd_battery_used_kwh': sum(cd_battery_used_kwh_i),
            'cd_fuel_mpgge': np.sum(weights) / np.sum(np.divide(weights, cd_fuel_mpgge_i, out=np.zeros_like(cd_fuel_mpgge_i), where=cd_fuel_mpgge_i!=0, casting='unsafe')),
            'cd_fuel_mpgde': np.sum(weights) / np.sum(np.divide(weights, cd_fuel_mpgde_i, out=np.zeros_like(cd_fuel_mpgde_i), where=cd_fuel_mpgde_i!=0, casting='unsafe')),
            'cd_electric_mpgge': np.sum(weights) / np.sum(np.divide(weights, cd_electric_mpgge_i, out=np.zeros_like(cd_electric_mpgge_i), where=cd_electric_mpgge_i!=0, casting='unsafe')),
            'cd_grid_electric_mpgge': np.sum(weights) / np.sum(np.divide(weights, cd_grid_electric_mpgge_i, out=np.zeros_like(cd_grid_electric_mpgge_i), where=cd_grid_electric_mpgge_i!=0, casting='unsafe')),
            'cd_electric_kwh__mi': np.sum(weights) / np.sum(np.divide(weights, cd_electric_kwh__mi_i, out=np.zeros_like(cd_electric_kwh__mi_i), where=cd_electric_kwh__mi_i!=0, casting='unsafe')),
            'cd_fuel_kwh__mi': np.sum(weights) / np.sum(np.divide(weights, cd_fuel_kwh__mi_i, out=np.zeros_like(cd_fuel_kwh__mi_i), where=cd_fuel_kwh__mi_i!=0, casting='unsafe')),
        }
        # also report: AveCombinedkWhperMile = UF*(CDelectricityKWhperMile + CDfuelKWhpermile) + (1-UF)*CSfuelKWhperMile
        uf = run_scenario.get_phev_util_factor(scenario, v, mpgge)
        mpgge_comp['ave_combined_kwh__mile'] = uf * (mpgge_comp['cd_electric_kwh__mi'] + mpgge_comp['cd_fuel_kwh__mi']) + (1-uf) * mpgge_comp['cs_fuel_kwh__mi']
    else:
        mpgge_i = np.array([m['mpgge'] for m in mpgges])
        grid_mpgge_i = np.array([m['grid_mpgge'] for m in mpgges])
        mpgde_i = np.array([m['mpgde'] for m in mpgges])
        kwh_per_m_i = np.array([m['kwh_per_mi'] for m in mpgges])
        mpgge_comp = {
            'mpgge': np.sum(weights) / np.sum(np.divide(weights, mpgge_i, out=np.zeros_like(mpgge_i), where=mpgge_i!=0, casting='unsafe')),
            'grid_mpgge': np.sum(weights) / np.sum(np.divide(weights, grid_mpgge_i, out=np.zeros_like(grid_mpgge_i), where=grid_mpgge_i!=0, casting='unsafe')),
            'mpgde': np.sum(weights) / np.sum(np.divide(weights, mpgde_i, out=np.zeros_like(mpgde_i), where=mpgde_i!=0, casting='unsafe')),
            # energy consumption kWh/mi is wt-averaged normally (doesn't require inverting / harmonic averaging)
            'kwh_per_mi': np.sum(weights) / np.sum(np.divide(weights, kwh_per_m_i, out=np.zeros_like(kwh_per_m_i), where=kwh_per_m_i!=0, casting='unsafe')),
        }

    if diagnostic: return mpgge_comp, sim_drives, mpgges
    return mpgge_comp, sim_drives


# %% 
if __name__=='__main__':


    vehicle_input_path  =Path(gl.T3CO_INPUTS_DIR / "tda_example/TDA_FY22_vehicle_model_assumptions.csv").resolve()
    scenario_inputs_path=Path(gl.T3CO_INPUTS_DIR / "tda_example/TDA_FY22_scenario_assumptions.csv").resolve()
    # load the generated file of vehicles, drive cycles, and tech targets
    PHEV = 365
    v = run_scenario.get_vehicle(PHEV, vehicle_input_path)
    scenario, cycle = run_scenario.get_scenario_and_cycle(PHEV, scenario_inputs_path)
    # cycle = cycle[2][0]
    cyc_file_path = gl.OPTIMIZATION_DRIVE_CYCLES / 'regional_haul.csv'
    cycle = run_scenario.load_design_cycle_from_path(cyc_file_path)

   
    mpgge_comp, sim_drives, mpgges = get_mpgge(cycle, v, scenario, diagnostic=True)
    get_range_mi(mpgge_comp, v, scenario)
    print('phev_utility_factor_override', scenario.phev_utility_factor_override)
    print('phev_utility_factor_computed', scenario.phev_utility_factor_computed)

    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(9,11))

    x = range(0, len(cycle.time_s))
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.plot(x, cycle.mps, label='cycle MPS')
    ax1.plot(x, sim_drives[0].mps_ach , label='MPS ach')
    ax1.set_title("drive cycle MPS and MPS achieved", color='white')
    fig.legend()


    x = range(0, len(cycle.time_s))
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    ax2.plot(x, sim_drives[0].mc_mech_kw_out_ach , label='CD mc_mech_kw_out_ach ')
    ax2.plot(x, sim_drives[1].mc_mech_kw_out_ach , label='CS mc_mech_kw_out_ach ')
    ax2.set_title("CD & CS motor kw out", color='white')
    fig.legend()

    x = range(0, len(cycle.time_s))
    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')
    ax3.plot(x, sim_drives[0].fc_kw_out_ach, label='CD fc_kw_out_ach')
    ax3.plot(x, sim_drives[1].fc_kw_out_ach, label='CS fc_kw_out_ach')
    ax3.set_title("CD & CS fuel converter kw out", color='white')
    fig.legend()

    # next plot
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, figsize=(18,18))

    CD = 0
    CS = 1

    x = range(0, len(cycle.time_s))
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.plot(x, sim_drives[0].mc_mech_kw_out_ach, dashes=[6, 2], label='CD mc_mech_kw_out_ach ')
    ax1.plot(x, sim_drives[0].fc_kw_out_ach, label='CD fc_kw_out_ach')
    ax1.plot(x, np.array(sim_drives[0].mc_mech_kw_out_ach) + np.array(sim_drives[0].fc_kw_out_ach), label='CD fc_kw_out_ach + mc_mech_kw_out_ach')
    ax1.set_title("CD motor and FC kw out", color='white')
    fig.legend()

    x = range(0, len(cycle.time_s))
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    mk_kwh_out = np.array(sim_drives[0].mc_mech_kw_out_ach) / 3600
    fc_kwh_out = np.array(sim_drives[0].fc_kw_out_ach) / 3600
    mc_kwh_cummultive = np.cumsum(np.array(sim_drives[0].mc_mech_kw_out_ach))/3600 
    fc_kwh_cummultive = np.cumsum(np.array(sim_drives[0].fc_kw_out_ach))/3600 
    ax2.plot(x, mc_kwh_cummultive, dashes=[6, 2], label='CD MC mech_KWH_out cummulative')
    ax2.plot(x, fc_kwh_cummultive, label='CD FC KWH_out cummulative')
    ax2.plot(x, mc_kwh_cummultive + fc_kwh_cummultive, label=f'CD ALL KWH_out cummulative kwh')
    ax2.set_title(f"CD KWH_out cummulative {round(sum(mk_kwh_out + fc_kwh_out))}" , color='white')
    fig.legend()

    x = range(0, len(cycle.time_s))
    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')
    ax3.plot(x, sim_drives[1].mc_mech_kw_out_ach, dashes=[6, 2], label='CS mc_mech_kw_out_ach ')
    ax3.plot(x, sim_drives[1].fc_kw_out_ach, label='CS fc_kw_out_ach')
    ax3.plot(x, np.array(sim_drives[1].mc_mech_kw_out_ach) + np.array(sim_drives[1].fc_kw_out_ach), label='CS fc_kw_out_ach + mc_mech_kw_out_ach')
    ax3.set_title("CS motor and FC kw out", color='white')
    fig.legend()

    x = range(0, len(cycle.time_s))
    ax4.tick_params(axis='x', colors='white')
    ax4.tick_params(axis='y', colors='white')
    mk_kwh_out = np.array(sim_drives[1].mc_mech_kw_out_ach) / 3600
    fc_kwh_out = np.array(sim_drives[1].fc_kw_out_ach) / 3600
    mc_kwh_cummultive = np.cumsum(np.array(sim_drives[1].mc_mech_kw_out_ach))/3600 
    fc_kwh_cummultive = np.cumsum(np.array(sim_drives[1].fc_kw_out_ach))/3600 
    ax4.plot(x, mc_kwh_cummultive, dashes=[6, 2], label='CS MC mech_KWH_out cummulative')
    ax4.plot(x, fc_kwh_cummultive, label='CS FC KWH_out cummulative')
    ax4.plot(x, mc_kwh_cummultive + fc_kwh_cummultive, label=f'CS ALL KWH_out cummulative kwh')
    ax4.set_title(f"CS KWH_out cummulative {round(sum(mk_kwh_out + fc_kwh_out))}", color='white')
    fig.legend()

    cd_elec_kwh_out_ach = round(sum(np.array(sim_drives[CD].ess_kw_out_ach) / 3600),1)
    cd_fuel_kwh_out_ach = round(sum(sim_drives[CD].fs_kwh_out_ach),1) 
    cs_elec_kwh_out_ach = round(sum(np.array(sim_drives[CS].ess_kw_out_ach) / 3600),1)
    cs_fuel_kwh_out_ach = round(sum(sim_drives[CS].fs_kwh_out_ach),1)
    
    print(f'total CD Mode electricity used (from ess_kw_out) {cd_elec_kwh_out_ach}')
    print(f'total CD Mode fuel used (from fs_kwh_out) {cd_fuel_kwh_out_ach}')
    print(f'total CS Mode electricity used (from ess_kw_out) {cs_elec_kwh_out_ach}')
    print(f'total CS Mode fuel used (from fs_kwh_out) {cs_fuel_kwh_out_ach}')
    cd_elec_mpgge  = round(sum(sim_drives[CD].dist_mi) / (cd_elec_kwh_out_ach / gl.get_kwh_per_gge()),1)
    print(f'CD mode cd_fuel_mpgge {round(sim_drives[CD].mpgge,1)}')
    print(f'CD mode cd_electric_mpgge {cd_elec_mpgge}')
    print(f'CD mode cd_grid_electric_mpgge {cd_elec_mpgge*v.chg_eff}')
    print(f'CS mode cs_fuel_mpgge {round(sim_drives[CS].mpgge,1)}')
    
    # # %%
    # sel=328
    # selections = [sel]
    # PHEV = 328
    # dir_mark = f"../../run_scripts/PHEV-testing/results/{sel}"
    # vehicles = "../../run_scripts/external_resources/phev-testing/TDA_FY22_vehicle_model_assumptions.csv"
    # scenarios = "../../run_scripts/external_resources/phev-testing/TDA_FY22_scenario_assumptions.csv"
    # Path('../../results/tco-ints/').mkdir(parents=True, exist_ok=True)
    # Path('../../results/tco-results/').mkdir(parents=True, exist_ok=True)
    # gl.TCO_INTERMEDIATES = Path('../../results/tco-ints/')
    # gl.TCO_RESULTS = Path('../../results/tco-results/')
    # gl.write_files = True

    # v = run_scenario.get_vehicle(PHEV, vehicles)
    # scenario, cycle = run_scenario.get_scenario_and_cycle(PHEV, scenarios)
    # cycle = cycle[0][0]

    # mpgge_comp, sim_drives, mpgges = get_mpgge(cycle, v, scenario, diagnostic=True)
    # get_range_mi(mpgge_comp, v, scenario)

    # cd_elec_kwh_out_ach = round(sum(np.array(sim_drives[CD].ess_kw_out_ach) / 3600),1)
    # cd_fuel_kwh_out_ach = round(sum(sim_drives[CD].fs_kwh_out_ach),1) 
    # cs_elec_kwh_out_ach = round(sum(np.array(sim_drives[CS].ess_kw_out_ach) / 3600),1)
    # cs_fuel_kwh_out_ach = round(sum(sim_drives[CS].fs_kwh_out_ach),1)
    # print(f'total CD Mode electricity used (from ess_kw_out) {cd_elec_kwh_out_ach}')
    # print(f'total CD Mode fuel used (from fs_kwh_out) {cd_fuel_kwh_out_ach}')
    # print(f'total CS Mode electricity used (from ess_kw_out) {cs_elec_kwh_out_ach}')
    # print(f'total CS Mode fuel used (from fs_kwh_out) {cs_fuel_kwh_out_ach}')
    # print('++++')
    
    # cd_elec_mpgge  = round(sum(sim_drives[CD].dist_mi) / (cd_elec_kwh_out_ach / gl.get_kwh_per_gge()),1)
    
    # print(f'CD mode cd_fuel_mpgge {round(sim_drives[CD].mpgge,1)}')
    # print(f'CD mode cd_electric_mpgge {cd_elec_mpgge}')
    # print(f'CD mode cd_grid_electric_mpgge {cd_elec_mpgge*v.chg_eff}')
    # print(f'CS mode cs_fuel_mpgge {round(sim_drives[CS].mpgge,1)}')

# %%
