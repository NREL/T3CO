# Table of Contents

* [objectives.gradeability](#objectives.gradeability)
  * [get\_gradeability](#objectives.gradeability.get_gradeability)

<a id="objectives.gradeability"></a>

# objectives.gradeability

<a id="objectives.gradeability.get_gradeability"></a>

#### get\_gradeability

```python
def get_gradeability(analysis_vehicle,
                     scenario=None,
                     verbose=False,
                     ess_init_soc=None,
                     set_weight_to_max_kg=True)
```

This function runs SimDrives to determine the gradeability at given speed and the grade vehicle is
evaluated at how much it meets or exceeds target speed at the target grade.

**Arguments**:

- `analysis_vehicle` _fastsim.vehicle.Vehicle_ - FASTSim vehicle object for analysis vehicle
- `scenario` _run_scenario.Scenario, optional_ - Scenario object for current selection. Defaults to None.
- `verbose` _bool, optional_ - if True, prints process steps. Defaults to False.
- `ess_init_soc` _float, optional_ - ESS Initial SOC override. Defaults to None.
- `set_weight_to_max_kg` _bool, optional_ - if True, run_scenario.set_test_weight() overrides vehice weight to GVWR. Defaults to True.
  

**Returns**:

- `grade_6percent_mph_ach` _float_ - Achieved speed on 6% grade test
- `grade_1pt25percent_mph_ach` _float_ - Achieved speed on 1.25% grade test
- `grade_6_simdrive` _fastsim.simdrive.SimDrive_ - FASTSim SimDrive for gradeability test of 6% grade
- `grade_125_simdrive` _fastsim.simdrive.SimDrive_ - FASTSim SimDrive for gradeability test of 1.25% grade

