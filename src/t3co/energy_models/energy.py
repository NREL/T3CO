from dataclasses import dataclass
from t3co.energy_models.fastsim.fastsim_wrapper import RunFastsim
from t3co.input_data.scenario import Scenario
from t3co.input_data.vehicle import Vehicle
from t3co.constants import Global as gl

@dataclass
class Energy():
    mpgge: float = None
    primary_fuel_range_mi: float = None

    def __init__(self, sim_model: str, mpgge: float = None, primary_fuel_range_mi:float = None):
        if mpgge and primary_fuel_range_mi:
            self.mpgge = mpgge
            self.primary_fuel_range_mi = primary_fuel_range_mi
        else:
            if sim_model=='fastsim':
                self.run_fastsim_model()

    def run_fastsim_model(self, vehicle: Vehicle, scenario: Scenario):
        fastsim_run = RunFastsim(vehicle=vehicle, scenario=scenario)
        self.mpgge = fastsim_run.simdrive.mpgge
        # kwh_per_gge = gl.kwh_per_gge
        if vehicle.veh_pt_type == gl.BEV:
            # assert (
            #     vehicle.fs_kwh == 0 and vehicle.fc_max_kw == 0
            # ), "Error! BEV vehicle has non-zero ICE attributes - vehicle mass calculation may be off"
            # mpgge = mpgge_info["mpgge"]  # use fuel efficiency from battery
            range_mi = (
                vehicle.ess_max_kwh
                * (fastsim_run.simdrive.veh.max_soc - fastsim_run.simdrive.veh.min_soc)
                * self.mpgge
                / gl.kwh_per_gge
            )
            self.primary_fuel_range_mi = range_mi
        elif vehicle.veh_pt_type == gl.CONV:
            # assert (
            #     vehicle.ess_max_kwh == 0 and vehicle.mc_max_kw == 0
            # ), "Error! CONV vehicle has non-zero BEV attributes - vehicle mass calculation may be off"
            # mpgge = mpgge_info["mpgge"]
            range_mi = (vehicle.fs_kwh / gl.kwh_per_gge) * self.mpgge
            self.primary_fuel_range_mi = range_mi
        elif vehicle.veh_pt_type == gl.HEV:
            elec_range_mi = (
                fastsim_run.simdrive.veh.ess_max_kwh
                * (fastsim_run.simdrive.veh.max_soc - fastsim_run.simdrive.veh.min_soc)
                * self.mpgge
                / gl.kwh_per_gge
            )
            conv_range_mi = (vehicle.fs_kwh / gl.kwh_per_gge) * self.mpgge
            range_mi = elec_range_mi + conv_range_mi
            self.primary_fuel_range_mi = range_mi