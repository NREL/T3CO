import ast
import sys
from pathlib import Path

import fastsim
import numpy as np
from typing import List, Union

from t3co.constants import Global as gl
from t3co.input_data.scenario import Scenario


class RunFastsim:
    vehicle: fastsim.vehicle.Vehicle = None
    cycles: Union[fastsim.cycle.Cycle, List[fastsim.simdrive.SimDrive]] = None
    simdrives: Union[fastsim.simdrive.SimDrive, List[fastsim.simdrive.SimDrive]] = None
    mpgge: float = None
    range_mi: float = None

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the RunFastsim class.
        """
        instance = super(RunFastsim, cls).__new__(cls)
        return instance
    
    def __init__(
        self,
        veh_no: int,
        scenario: Scenario,
        veh_input_path: Union[str, Path] = gl.RESOURCES_FOLDERPATH
        / "inputs"
        / "Demo_FY22_vehicle_model_assumptions.csv",
        use_rust: bool = True,
    ) -> None:
        self.load_vehicle(veh_no=veh_no, veh_input_path=veh_input_path, use_rust=use_rust)
        self.cycles = self.load_design_cycle_from_scenario(scenario=scenario, return_rustcycle=use_rust)

        if isinstance(self.cycles, list):
            self.simdrives, mpgges_list, weights = [], [], []
            scenario.constant_trip_distance_mi = 0
            for i in range(len(self.cycles)):
                scenario.constant_trip_distance_mi += (
                    sum(
                        self.cycles[i][0].mph
                        * np.diff(np.array(self.cycles[i][0].time_s), append=0)
                    )
                    * self.cycles[i][1]
                    / 3600
                )
                self.simdrives.append(self.get_simdrive(cycle=self.cycles[i][0]))
                mpgges_list.append(self.simdrives[i].mpgge)
                weights.append(self.cycles[i][1])

            mpgges_list = np.array(mpgges_list)
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
                ),
            )
        else:
            scenario.constant_trip_distance_mi = (
                sum(self.cycles.mph * np.diff(np.array(self.cycles.time_s), append=0))
                / 3600
            )
            self.simdrives = self.get_simdrive(cycle=self.cycles)
            self.mpgge = self.simdrives.mpgge

        self.get_range()

    def load_vehicle(self, veh_no: int, veh_input_path: Union[str, Path], use_rust:bool = True) -> fastsim.vehicle.Vehicle:
        """
        Loads vehicle object from vehicle number and input CSV filepath.

        Args:
            veh_no (int): Vehicle selection number.
            veh_input_path (Union[str, Path]): Vehicle model assumptions input CSV file path.

        Returns:
            fastsim.vehicle.Vehicle: FASTSim vehicle object.
        """
        scenario_sel = int(float(str(veh_no).split("_")[0]))
        self.vehicle = fastsim.vehicle.Vehicle.from_vehdb(
            scenario_sel, veh_input_path, to_rust=use_rust
        )
        self.vehicle.set_derived()
        self.vehicle.set_veh_mass()

    def load_design_cycle_from_scenario(
        self,
        scenario: Scenario,
        cyc_file_path: Union[str, Path] = gl.CYCLES_FOLDER,
        return_rustcycle: bool = True
    ) -> Union[fastsim.cycle.Cycle, List[fastsim.cycle.Cycle]]:
        """
        Loads the design cycle used for mpgge and range determination.

        Args:
            scenario (Scenario): Scenario object for current selection.
            cyc_file_path (Union[str, Path], optional): Drive cycle input file path. Defaults to gl.CYCLES_FOLDER.

        Returns:
            Union[fastsim.cycle.Cycle, List[fastsim.cycle.Cycle]]: FASTSim cycle object for current Scenario object.
        """
        scenario.drive_cycle = (
            ast.literal_eval(scenario.drive_cycle)
            if not Path(scenario.drive_cycle).exists()
            else scenario.drive_cycle
        )
        if isinstance(scenario.drive_cycle, list):
            design_cycles = []
            weights = []
            for dc_weight in scenario.drive_cycle:
                if isinstance(dc_weight, tuple):
                    cycle_file_name, weight = dc_weight
                    cyc = self.load_design_cycle_from_path(
                        cyc_file_path=Path(cyc_file_path) / cycle_file_name,
                        return_rustcycle=return_rustcycle
                    )
                    cyc.name = cycle_file_name
                weights.append(weight)
                design_cycles.append((cyc, weight))
            if sum(weights) != 1:
                print(
                    f"Sum of weights for composite cycles (sum = {sum(weights)}) is not 1."
                )
                raise ValueError
            
            return design_cycles
        else:
            cycle_file_name = Path(scenario.drive_cycle).name
            design_cycles = self.load_design_cycle_from_path(
                cyc_file_path=scenario.drive_cycle,
                return_rustcycle=return_rustcycle
            )
            design_cycles.name = cycle_file_name
            return design_cycles

    def load_design_cycle_from_path(self, cyc_file_path: Union[str, Path], return_rustcycle: bool = True) -> Union[fastsim.cycle.RustCycle, fastsim.cycle.Cycle]:
        """
        Loads the Cycle object from the drive cycle filepath.

        Args:
            cyc_file_path (Union[str, Path]): Drive cycle input file path.

        Returns:
            fastsim.cycle.Cycle: FASTSim cycle object for current Scenario object.
        """
        if not Path(cyc_file_path).exists():
            print(
                f"Drive cycle not found in {cyc_file_path}, trying {gl.CYCLES_FOLDER}"
            )
            finalized_path = Path(gl.CYCLES_FOLDER) / cyc_file_path

        else:
            finalized_path = cyc_file_path
        cyc = fastsim.cycle.Cycle.from_file(finalized_path)
        if return_rustcycle:
            return cyc.to_rust()
        else:
            return cyc
        

    def get_simdrive(self, cycle: fastsim.cycle.Cycle) -> fastsim.fastsimrust.RustSimDrive:
        """
        Creates a SimDrive object for the given cycle and vehicle.

        Args:
            cycle (fastsim.cycle.Cycle): The drive cycle.

        Returns:
            fastsim.fastsimrust.RustSimDrive: The RustSimDrive object.
        """
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
        props.reset_orphaned()
        props.kwh_per_gge = gl.KWH_PER_GGE
        simdrive.props = props
        simdrive.sim_drive(init_soc=self.vehicle.max_soc)
        return simdrive

    def get_range(self) -> None:
        """
        Calculates the range of the vehicle based on its type and energy storage.
        """
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