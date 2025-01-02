import ast
from pathlib import Path
import fastsim
import numpy as np
from typing_extensions import List

from t3co.input_data.config import Config
from t3co.input_data.scenario import Scenario
from t3co.constants import Global as gl


class RunFastsim:
    vehicle: fastsim.vehicle.Vehicle = None
    cycles: fastsim.cycle.Cycle | List[fastsim.simdrive.SimDrive] = None
    simdrives: fastsim.simdrive.SimDrive | List[fastsim.simdrive.SimDrive] = None
    mpgge: float = None
    range_mi: float = None

    def __init__(
        self,
        veh_no: int,
        scenario: Scenario,
        config: Config = None,
        veh_input_path: str | Path = Path(__file__).resolve().parents[2]
        / "resources"
        / "inputs"
        / "Demo_FY22_vehicle_model_assumptions.csv",
    ) -> None:
        self.load_vehicle(veh_no=veh_no, veh_input_path=veh_input_path)
        self.cycles = self.load_design_cycle_from_scenario(
            scenario=scenario, config=config
        )

        if isinstance(self.cycles, list):
            self.simdrives, mpgges_list, weights = [], [], []
            scenario.constant_trip_distance_mi = 0
            for i in range(len(self.cycles)):
                scenario.constant_trip_distance_mi+=(
                    sum(
                        self.cycles[i][0].mph
                        * np.diff(np.array(self.cycles[i][0].time_s), append=0)
                    )
                    * self.cycles[i][1]
                    / 3600
                )
                # print(f'cycle: {self.cycles[i][0].mph}')
                self.simdrives.append(self.get_simdrive(cycle=self.cycles[i][0]))
                # print(f'self.simdrives[i].mpgge: {self.simdrives[i].mpgge}')
                mpgges_list.append(self.simdrives[i].mpgge)
                weights.append(self.cycles[i][1])

            mpgges_list = np.array(mpgges_list)
            # print(f'mpgges_list: {mpgges_list}')
            weights = np.array(weights)
            self.mpgge = np.divide(
                sum(weights), 
                np.sum(
                    np.divide(
                        weights,
                        mpgges_list,
                        out=np.zeros_like(mpgges_list),
                        where=mpgges_list != 0,
                        casting="unsafe",
                    )
                )
            )
        else:
            scenario.constant_trip_distance_mi = (
                sum(self.cycles.mph * np.diff(np.array(self.cycles.time_s), append=0))
                / 3600
            )
            self.simdrives = fastsim.simdrive.SimDrive(cyc=self.cycles)
            self.mpgge = self.simdrives.mpgge
        
        self.get_range()

    def load_vehicle(self, veh_no: int, veh_input_path: str) -> fastsim.vehicle.Vehicle:
        """
        This function loads vehicle object from vehicle number and input csv filepath

        Args:
            veh_no (int): vehicle selection number
            veh_input_path (str): vehicle model assumptions input CSV file path

        Returns:
            veh (fastsim.vehicle.Vehicle): FASTSim vehicle object
        """

        scenario_sel = int(float(str(veh_no).split("_")[0]))
        self.vehicle = fastsim.vehicle.Vehicle.from_vehdb(scenario_sel, veh_input_path, to_rust=True)
        self.vehicle.set_derived()
        self.vehicle.set_veh_mass()
        # print(f'vehicle: {self.vehicle.__dict__}')

    def load_design_cycle_from_scenario(
        self,
        scenario: Scenario,
        config: Config = None,
        cyc_file_path: str = gl.OPTIMIZATION_DRIVE_CYCLES,
        do_input_validation: bool = False,
    ) -> fastsim.cycle.Cycle | List[fastsim.cycle.Cycle]:
        """
        This helper method loads the design cycle used for mpgge and range determination.
        It can also be used standalone to get cycles not in standard gl.OPTIMIZATION_DRIVE_CYCLES location,
        but still needs cycle name from scenario object, carried in scenario.drive_cycle.
        If the drive cycles are a list of tuples, handle accordingly with eval.

        Args:
            scenario (Scenario): Scenario object for current selection
            cyc_file_path (str, optional): drivecycle input file path. Defaults to gl.OPTIMIZATION_DRIVE_CYCLES.

        Returns:
            range_cyc (fastsim.cycle.Cycle): FASTSim cycle object for current Scenario object
        """

        if config:
            if config.dc_files != None and not do_input_validation:
                dc_id = int(float(str(scenario.selection).split("_")[1]))
                sdc = str(config.dc_files[dc_id])
        else:
            sdc = str(scenario.drive_cycle)
        if "[" in sdc and "]" in sdc and "(" in sdc and ")" in sdc:
            scenario.drive_cycle = ast.literal_eval(sdc)
            range_cyc = []
            for dc_weight in scenario.drive_cycle:
                cycle_file_name = Path(dc_weight[0]).name
                cyc = self.load_design_cycle_from_path(
                    cyc_file_path=Path(cyc_file_path) / dc_weight[0]
                )
                cyc.name = cycle_file_name
                weight = dc_weight[1]
                range_cyc.append((cyc, weight))
            return range_cyc
        else:
            cycle_file_name = Path(sdc).name
            range_cyc = self.load_design_cycle_from_path(cyc_file_path=sdc)
            range_cyc.name = cycle_file_name
            return range_cyc

    def load_design_cycle_from_path(self, cyc_file_path: str):
        """
        This helper method loads the Cycle object from the drivecycle filepath

        Args:
            cyc_file_path (str): drivecycle input file path

        Returns:
            range_cyc (fastsim.cycle.Cycle): FASTSim cycle object for current Scenario object
        """
        if Path(cyc_file_path).exists() == False:
            print(
                f"Drive cycle not found in {cyc_file_path}, trying {gl.OPTIMIZATION_DRIVE_CYCLES}"
            )
            finalized_path = Path(gl.OPTIMIZATION_DRIVE_CYCLES) / cyc_file_path

        else:
            finalized_path = cyc_file_path
        cyc = fastsim.cycle.Cycle.from_file(finalized_path)
        cyc = cyc.to_rust()
        return cyc

    def get_simdrive(self, cycle:fastsim.cycle.Cycle):
        simdrive = fastsim.simdrive.SimDrive(cycle, self.vehicle)
        simdrive = simdrive.to_rust()

        sim_params = simdrive.sim_params
        sim_params.reset_orphaned()
        sim_params.missed_trace_correction = False
        sim_params.trace_miss_speed_mps_tol = np.inf
        sim_params.energy_audit_error_tol = np.inf
        sim_params.trace_miss_dist_tol = np.inf
        simdrive.sim_params = sim_params

        props = simdrive.props
        props.reset_orphaned()  # see if this is needed
        props.kwh_per_gge = gl.KWH_PER_GGE
        simdrive.props = props
        simdrive.sim_drive(init_soc=self.vehicle.max_soc)
        return simdrive
    
    def get_range(self):
        if self.vehicle.veh_pt_type == gl.BEV:
            self.range_mi = (
                self.vehicle.ess_max_kwh
                * (self.vehicle.max_soc - self.vehicle.min_soc)
                * self.mpgge
                / gl.KWH_PER_GGE
            )

        elif self.vehicle.veh_pt_type == gl.CONV:
            self.range_mi = (self.vehicle.fs_kwh / gl.KWH_PER_GGE) * self.mpgge

        elif self.vehicle.veh_pt_type == gl.HEV:
            elec_range_mi = (
                self.vehicle.ess_max_kwh
                * (self.vehicle.max_soc - self.vehicle.min_soc)
                * self.mpgge
                / gl.KWH_PER_GGE
            )
            conv_range_mi = (self.vehicle.fs_kwh / gl.KWH_PER_GGE) * self.mpgge
            self.range_mi = elec_range_mi + conv_range_mi
