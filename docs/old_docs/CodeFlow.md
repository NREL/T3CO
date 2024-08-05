# General Code Flow

- Generally, start things off in `sweep.py` with a command like 
    ```
    python sweep.py -selections [23,24,25,26] -vehicles /path/to/vehiclesfile.csv -scenarios /path/to/scenariosfile.csv
    ```
    The `-vehicles` argument points to the vehicles input file.
    The `-scenarios` argument points to the scenarios input file.
    These two files are linked with an index column called `selection`, representing the row from each file to use. [`FASTSim Vehicles`](https://github.com/NREL/fastsim/blob/5910d9d610dd0760b015d78274c97308d3696798/python/fastsim/vehicle.py#L145) and [`Scenarios`](https://github.com/NREL/T3CO-private/blob/52252a06fd16cc7bae377f169b78d02c30887b96/t3co/run/run_scenario.py#L271) are the core data structures in **T3CO**
    
     Example of [Scenario inputs](./ScenarioFile.md).
     
     Example of [FASTSim vehicle inputs](https://github.com/NREL/fastsim/blob/fastsim-2/python/fastsim/resources/FASTSim_py_veh_db.csv).
     
- [Sweep Code](https://github.com/NREL/T3CO-private/blob/52252a06fd16cc7bae377f169b78d02c30887b96/t3co/sweep.py#L406C5-L406C26) sweeps through selected scenarios, in this case `[23,24,25,26]`
- `for selection, scenario_name in vehicles.index, vehicles.scenario_name`
  - `if selection in [23,24,25,26]: optimize(selection, scenario_name)` [link](https://github.com/NREL/T3CO-private/blob/52252a06fd16cc7bae377f169b78d02c30887b96/t3co/sweep.py#L573) 
  - `optimize` can optimize the vehicle and scenario, or it can skip optimizing compute TCO from vehicle and scenario inputs and report that
  - `if optimizing`
    - `run_moo(selection int, scenarios DataFrame, *args, **kwargs)` [link](https://github.com/NREL/T3CO-private/blob/52252a06fd16cc7bae377f169b78d02c30887b96/t3co/sweep.py#L316)
    - get [get knobs-bounds & curves](https://github.com/NREL/T3CO-private/blob/52252a06fd16cc7bae377f169b78d02c30887b96/t3co/sweep.py#L138)
      - note: optimization parameters (knobs) are implicitly activated by their minimum and maximum bounds being populated. See [Scenario inputs](./ScenarioFile.md). For example, if the row for your selection has populated values in columns `knob_min_ess_kwh` and `knob_max_ess_kwh` then that tells the optimizer that battery size, `ess_kwh`, is an optimization parameter (knob). The curves work the same way, for example `eng_eff_imp_curve_sel` being populated means that the opimization parameter for engine efficiency should be used.
    - get [objectives and constraints](https://github.com/NREL/T3CO-private/blob/52252a06fd16cc7bae377f169b78d02c30887b96/t3co/sweep.py#L274)
      - note: unlike knobs, constraints need to be explicitly turned on with `True`. For example: The Scenario file will have `constraint_range` value of `True`, and by necessity the target range must be specified as well, in `target_range_mi` 
    - begin optimization [loop](https://github.com/NREL/T3CO-private/blob/52252a06fd16cc7bae377f169b78d02c30887b96/t3co/moopack/moo.py#L1123)


```
while lowest TCO not found by PyMoo, for, say, vehicle & selection 23:
  ______________________________                                                                                                    ┌────────────────┐
 ╱                              ╲                                                                                                   │return optimized│
╱ lowest TCO found while meeting ╲__________________________________________________________________________________________________│parameters      │
╲ grade and accel constraints    ╱yes                                                                                               └────────┬───────┘
 ╲______________________________╱                                                                                                                
                │no                                                                                                                              
     ___________▽___________     ┌──────────────────────────────────────────────┐                                                                
    ╱                       ╲    │try new chassis weight, code:                 │                                                                
   ╱ chassis light-weighting ╲___│weight_delta_percent_knob(wt_delta_perc_guess,│                                                                
   ╲ knob active             ╱yes│optvehicle)                                   │                                                                
    ╲_______________________╱    └───────────────────────┬──────────────────────┘                                                                
                │no                                      │                                                                                       
                └──────────┬─────────────────────────────┘                                                                                       
                     ______▽_______     ┌──────────────────────────────────────────┐                                                             
                    ╱              ╲    │try new drag coeff, code:                 │                                                             
                   ╱ CdA drag coeff ╲___│cda_percent_delta_knob(CdA_reduction_perc,│                                                             
                   ╲ knob active    ╱yes│optvehicle)                               │                                                             
                    ╲______________╱    └─────────────────────┬────────────────────┘                                                             
                           │no                                │                                                                                  
                           └─────────┬────────────────────────┘                                                                                  
                             ________▽________     ┌─────────────────────────────────────┐                                                       
                            ╱                 ╲    │try new peak engine efficiency, code:│                                                       
                           ╱ engine efficiency ╲___│fc_peak_eff_knob(fc_peak_eff_guess,  │                                                       
                           ╲ knob active       ╱yes│optvehicle)                          │                                                       
                            ╲_________________╱    └──────────────────┬──────────────────┘                                                       
                                     │no                              │                                                                          
                                     └────────┬───────────────────────┘                                                                          
                                       _______▽________     ┌──────────────────────────────────────┐                                             
                                      ╱                ╲    │try new engine size [kw], code:       │                                             
                                     ╱ engine size [kw] ╲___│run_scenario.set_max_fuel_converter_kw│                                             
                                     ╲ knob active      ╱yes└───────────────────┬──────────────────┘                                             
                                      ╲________________╱                        │                                                                
                                              │no                               │                                                                
                                              └────────┬────────────────────────┘                                                                
                                               ________▽________     ┌───────────────────────────────────────────┐                               
                                              ╱                 ╲    │try new fuel store size [kwh], code:       │                               
                                             ╱ fuel store size   ╲___│run_scenario.set_fuel_store_kwh(optvehicle,│                               
                                             ╲ [kwh] knob active ╱yes│fs_kwh_guess)                              │                               
                                              ╲_________________╱    └─────────────────────┬─────────────────────┘                               
                                                       │no                                 │                                                     
                                                       └─────────┬─────────────────────────┘                                                     
                                                         ________▽________     ┌────────────────────────────────────────────┐                    
                                                        ╱                 ╲    │try new battery size [kwh], code:           │                    
                                                       ╱ battery size      ╲___│run_scenario.set_max_battery_kwh(optvehicle,│                    
                                                       ╲ [kwh] knob active ╱yes│max_ess_kwh_guess)                          │                    
                                                        ╲_________________╱    └──────────────────────┬─────────────────────┘                    
                                                                 │no                                  │                                          
                                                                 └─────────┬──────────────────────────┘                                          
                                                                    _______▽________     ┌─────────────────────────────────────────┐             
                                                                   ╱                ╲    │try new motor power [kw], code:          │             
                                                                  ╱ motor power [kw] ╲___│run_scenario.set_max_motor_kw(optvehicle,│             
                                                                  ╲ knob active      ╱yes│self.opt_scenario, max_motor_kw_guess)   │             
                                                                   ╲________________╱    └────────────────────┬────────────────────┘             
                                                                           │no                                │                                  
                                                                           └─────────────────┬────────────────┴─     
                                                                                ┌────────────▽───────────┐                                            
                                                                                │compute TCO and, if     │                                            
                                                                                │applicable, acceleration│                                            
                                                                                │and grade performance   │                                            
                                                                                └────────────┬───────────┘                                            
                                                                                ┌────────────▽────────────┐                                           
                                                                                │Optimizer keeps cycling  │                                           
                                                                                │trying to find lowest TCO│                                           
                                                                                └─────────────────────────┘                                           
```














diagrams generated with https://arthursonzogni.com/Diagon/#Flowchart

