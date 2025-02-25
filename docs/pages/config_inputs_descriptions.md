# Config Input Parameters

<div class="filter-container">
    <span><strong>Filter Options: Units:</strong></span>
    <select id="configUnitsFilter"><option value="">All</option></select>
    <span><strong>Data Type:</strong></span>
    <select id="configdatatypeFilter"><option value="">All</option></select>
    <div class="button-container">
        <button id="downloadTemplateBtn">Download Config Template</button>
    </div>
</div>
<div class="table-container">
    <table id="configTable">
        <thead>
            <tr>
                <th>Config Input Parameter</th>
                <th>Full Form</th>
                <th>Units</th>
                <th>Description</th>
                <th>Data Type</th>
            </tr>
        </thead>
    <tbody>
        <tr>
            <td>analysis_id</td>
            <td>Analysis Index</td>
            <td></td>
            <td>Index for managing T3CO analyses   or runs</td>
            <td>int</td>
        </tr>
        <tr>
            <td>analysis_name</td>
            <td>Analysis Name</td>
            <td></td>
            <td>Name of T3CO Analysis for user&#39;s   reference</td>
            <td>string</td>
        </tr>
        <tr>
            <td>vehicle_file</td>
            <td>Vehicle Filepath</td>
            <td></td>
            <td>Filepath to vehicle input file   either absolute or relative to /resources/ folder</td>
            <td>string</td>
        </tr>
        <tr>
            <td>scenario_file</td>
            <td>Scenario Filepath</td>
            <td></td>
            <td>Filepath to scenario input file   either absolute or relative to /resources/ folder</td>
            <td>string</td>
        </tr>
        <tr>
            <td>dst_dir</td>
            <td>Destination Directory</td>
            <td></td>
            <td>Filepath to results destination   directory either absolute or relative to /resources/ folder</td>
            <td>string</td>
        </tr>
        <tr>
            <td>selections</td>
            <td>Selections List</td>
            <td></td>
            <td>List of selections from   vehicle/scenario files to include in the analysis. Takes input as an integer   or list of integers. &#39;-1&#39; makes T3CO run all vehicles in the vehicle file</td>
            <td>int/list</td>
        </tr>
        <tr>
            <td>vehicle_life_yr</td>
            <td>Vehicle Life</td>
            <td>yr</td>
            <td>Override number of TCO years for   all selections.. If left blank, T3CO uses selection specific vehicle_life_yr   from scenario file</td>
            <td>int</td>
        </tr>
        <tr>
            <td>ess_max_charging_power_kw</td>
            <td>ESS Max Charging Power Override</td>
            <td>kW</td>
            <td>Override ESS max charging power   for all selections. If left blank, T3CO uses selection specific   ess_max_charging_power_kw from scenario file</td>
            <td>float</td>
        </tr>
        <tr>
            <td>fs_fueling_rate_kg_per_min</td>
            <td>Fuel Storage Gaseous Fueling Rate</td>
            <td>kg/min</td>
            <td>Override gaseous fueling fill   rate for all selections. If left blank, T3CO uses selection specific   fs_fueling_rate_kg_per_min from scenario file</td>
            <td>float</td>
        </tr>
        <tr>
            <td>fs_fueling_rate_gasoline_gpm</td>
            <td>Fuel Storage Gasoline Fueling Rate</td>
            <td>gal/min</td>
            <td>Override gasoline liquid fueling   fill rate for all selections. If left blank, T3CO uses selection specific   fs_fueling_rate_gasoline_gpm from scenario file</td>
            <td>float</td>
        </tr>
        <tr>
            <td>fs_fueling_rate_diesel_gpm</td>
            <td>Fuel Storage Diesel Fueling Rate</td>
            <td>gal/min</td>
            <td>Override diesel liquid fueling   fill rate for all selections. If left blank, T3CO uses selection specific   fs_fueling_rate_diesel_gpm from scenario file</td>
            <td>float</td>
        </tr>
        <tr>
            <td>algorithms</td>
            <td>Optimization Algorithms</td>
            <td></td>
            <td>Algorithm for pymoo   optimization. Select from    [&quot;NSGA2&quot;, &quot;PatternSearch&quot;]</td>
            <td>string</td>
        </tr>
        <tr>
            <td>lw_imp_curves</td>
            <td>Lightweighting Improvement Curves Filepath</td>
            <td></td>
            <td>Filepath to lightweighting   improvement cost curve either absolute or relative to /resources/ folder</td>
            <td>string</td>
        </tr>
        <tr>
            <td>eng_eff_imp_curves</td>
            <td>Engine Efficiency Improvement Curves Filepath</td>
            <td></td>
            <td>Filepath to engine efficiency   improvement cost curve either absolute or relative to /resources/ folder</td>
            <td>string</td>
        </tr>
        <tr>
            <td>aero_drag_imp_curves</td>
            <td>Aero Drag Coefficient Improvement   Curves Filepath</td>
            <td></td>
            <td>Filepath to aerodynamic drag   coefficient improvement cost curve either absolute or relative to /resources/   folder</td>
            <td>string</td>
        </tr>
        <tr>
            <td>lw_imp_curve_sel</td>
            <td>Lightweighting Improvement Curve   Selection Override</td>
            <td></td>
            <td>Override selection of light   weighting improvement curve from lw_imp_curves file for all selections</td>
            <td>string</td>
        </tr>
        <tr>
            <td>eng_eff_imp_curve_sel</td>
            <td>Engine Efficiency Improvement Curve   Selection Override</td>
            <td></td>
            <td>Override selection of engine   efficiency improvement curve from eng_eff_imp_curves file for all selections</td>
            <td>string</td>
        </tr>
        <tr>
            <td>aero_drag_imp_curve_sel</td>
            <td>Aero Drag Coefficient Improvement   Curve Selection Override</td>
            <td></td>
            <td>Override selection of   aerodynamic drag improvement curve from aero_drag_imp_curves file for all   selections</td>
            <td>string</td>
        </tr>
        <tr>
            <td>skip_all_opt</td>
            <td>Skip All Optimization</td>
            <td></td>
            <td>Boolean switch to override skip   optimization for all selections</td>
            <td>bool</td>
        </tr>
        <tr>
            <td>constraint_range</td>
            <td>Optimization Constraint: Range</td>
            <td></td>
            <td>Override boolean switch for   optimization range constraint for all selections - if left blank, T3CO uses   selection specific switch</td>
            <td>bool</td>
        </tr>
        <tr>
            <td>constraint_accel</td>
            <td>Optimization Constraint: Acceleration Test</td>
            <td></td>
            <td>Override boolean switch for   optimization acceleration constraint for all selections- if left blank, T3CO   uses selection specific switch</td>
            <td>bool</td>
        </tr>
        <tr>
            <td>constraint_grade</td>
            <td>Optimization Constraint: Gradeability Test</td>
            <td></td>
            <td>Override boolean switch for   optimization gradeability constraint for all selections- if left blank, T3CO   uses selection specific switch</td>
            <td>bool</td>
        </tr>
        <tr>
            <td>objective_tco</td>
            <td>Optimization Objective: Total Cost of Ownership</td>
            <td></td>
            <td>Override boolean switch for   optimization objective as TCO for all selections- if left blank, T3CO uses   selection specific switch</td>
            <td>bool</td>
        </tr>
        <tr>
            <td>constraint_c_rate</td>
            <td>Optimization Constraint: Charge Rate</td>
            <td></td>
            <td>Override boolean switch for   optimization charge rate constraint for all selections- if left blank, T3CO   uses selection specific switch</td>
            <td>bool</td>
        </tr>
        <tr>
            <td>constraint_trace_miss_dist_percent_on</td>
            <td>Optimization Constraint: Distance Trace Miss</td>
            <td></td>
            <td>Override boolean switch for   optimization distance trace miss percentage for all selections- if left   blank, T3CO uses selection specific switch</td>
            <td>bool</td>
        </tr>
        <tr>
            <td>activate_tco_payload_cap_cost_multiplier</td>
            <td>Override Switch to Calculate Payload   Capacity Cost Multiplier</td>
            <td></td>
            <td>Override boolean switch for lost   payload capacity opportunity cost calculations- if left blank, T3CO uses   selection specific switch</td>
            <td>bool</td>
        </tr>
        <tr>
            <td>activate_tco_fueling_dwell_time_cost</td>
            <td>Override Switch to Calculate   Fueling/Charging Dwell Time</td>
            <td></td>
            <td>Override boolean switch for   fueling dwell time opportunity cost calculations- if left blank, T3CO uses   selection specific switch</td>
            <td>bool</td>
        </tr>
        <tr>
            <td>fdt_frac_full_charge_bounds</td>
            <td>Fueling Dwell Time: Fractional   Charge SOC Bounds Override</td>
            <td></td>
            <td>Override fraction of lower and   upper bounds for fractional charge- if left blank, T3CO uses selection   specific switch</td>
            <td>list</td>
        </tr>
        <tr>
            <td>activate_mr_downtime_cost</td>
            <td>Override Switch to Calculate   Maintenance &amp; Repair Downtime</td>
            <td></td>
            <td>Override boolean switch for   maintenance and repair downtime opportunity cost calculations- if left blank,   T3CO uses selection specific switch</td>
            <td>bool</td>
        </tr>
    </tbody>
</table>
</div>