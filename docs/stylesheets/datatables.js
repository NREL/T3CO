document.addEventListener("DOMContentLoaded", function () {
    function setupDataTable(tableId, unitsFilterId, dataTypeFilterId, powertrainFilterId, t3coComponentFilterId, categoryFilterId, unitsColumn, dataTypeColumn, powertrainColumn, t3coComponentColumn, categoryColumn) {
        let table = new DataTable("#" + tableId, {
            paging: false,   // Show all rows
            searching: true, // Enable search
            ordering: true,  // Enable sorting
            info: false      // Hide table info
        });

        // Populate dropdowns with unique values
        function populateDropdown(columnIndex, dropdownId) {
            let uniqueValues = new Set();
            document.querySelectorAll(`#${tableId} tbody tr td:nth-child(${columnIndex})`).forEach(cell => {
                uniqueValues.add(cell.textContent.trim());
            });

            let dropdown = document.getElementById(dropdownId);
            dropdown.innerHTML = '<option value="">All</option>'; // Reset dropdown
            uniqueValues.forEach(value => {
                let option = document.createElement("option");
                option.value = value;
                option.textContent = value;
                dropdown.appendChild(option);
            });
        }

        if (unitsFilterId) {
            populateDropdown(unitsColumn, unitsFilterId);  // Units column
        }
        if (dataTypeFilterId) {
            populateDropdown(dataTypeColumn, dataTypeFilterId);  // Data Type column
        }
        // if (powertrainFilterId) {
        //     populateDropdown(powertrainColumn, powertrainFilterId);  // Powertrain column
        // }
        // if (t3coComponentFilterId) {
        //     populateDropdown(t3coComponentColumn, t3coComponentFilterId);  // T3CO Component column
        // }
        if (categoryFilterId) {
            populateDropdown(categoryColumn, categoryFilterId);  // Category column
        }

        // Apply filtering based on dropdown selection
        function filterTable() {
            let unitsValue = unitsFilterId ? document.getElementById(unitsFilterId).value.toLowerCase() : "";
            let dataTypeValue = dataTypeFilterId ? document.getElementById(dataTypeFilterId).value.toLowerCase() : "";
            let powertrainValue = powertrainFilterId ? document.getElementById(powertrainFilterId).value.toLowerCase() : "";
            let t3coComponentValue = t3coComponentFilterId ? document.getElementById(t3coComponentFilterId).value.toLowerCase() : "";
            let categoryValue = categoryFilterId ? document.getElementById(categoryFilterId).value.toLowerCase() : "";

            table.rows().every(function () {
                let row = this.node();
                let rowUnits = unitsColumn ? row.cells[unitsColumn - 1].textContent.toLowerCase() : "";
                let rowDataType = dataTypeColumn ? row.cells[dataTypeColumn - 1].textContent.toLowerCase() : "";
                let rowPowertrain = powertrainColumn ? row.cells[powertrainColumn - 1].textContent.toLowerCase() : "";
                let rowT3coComponent = t3coComponentColumn ? row.cells[t3coComponentColumn - 1].textContent.toLowerCase() : "";
                let rowCategory = categoryColumn ? row.cells[categoryColumn - 1].textContent.toLowerCase() : "";

                let matchUnits = unitsValue === "" || rowUnits === unitsValue;
                let matchDataType = dataTypeValue === "" || rowDataType === dataTypeValue;
                let matchPowertrain = powertrainValue === "" || rowPowertrain.includes(powertrainValue);
                let matchT3coComponent = t3coComponentValue === "" || rowT3coComponent.includes(t3coComponentValue);
                let matchCategory = categoryValue === "" || rowCategory === categoryValue;

                if (matchUnits && matchDataType && matchPowertrain && matchT3coComponent && matchCategory) {
                    this.nodes().to$().show();
                } else {
                    this.nodes().to$().hide();
                }
            });
        }

        if (unitsFilterId) {
            document.getElementById(unitsFilterId).addEventListener("change", filterTable);
        }
        if (dataTypeFilterId) {
            document.getElementById(dataTypeFilterId).addEventListener("change", filterTable);
        }
        if (powertrainFilterId) {
            document.getElementById(powertrainFilterId).addEventListener("change", filterTable);
        }
        if (t3coComponentFilterId) {
            document.getElementById(t3coComponentFilterId).addEventListener("change", filterTable);
        }
        if (categoryFilterId) {
            document.getElementById(categoryFilterId).addEventListener("change", filterTable);
        }
    }

    // Initialize the vehicle parameters table
    if (document.getElementById("vehicleTable")) {
        setupDataTable("vehicleTable", "unitsFilter", "datatypeFilter", "powertrainFilter", null, null, 3, 6, 5, null, null);
    }

    // Initialize the scenario parameters table
    if (document.getElementById("scenarioTable")) {
        setupDataTable("scenarioTable", "scenarioUnitsFilter", "scenariodatatypeFilter", "powertrainFilter", "t3coComponentFilter", null, 3, 7, 5, 6, null);
    }

    // Initialize the ledger parameters table
    if (document.getElementById("ledgerTable")) {
        setupDataTable("ledgerTable", "ledgerUnitsFilter", "ledgerdatatypeFilter", null, null, "ledgercategoryFilter", 4, 6, null, null, 2);
    }

    // Initialize the config parameters table
    if (document.getElementById("configTable")) {
        setupDataTable("configTable", "configUnitsFilter", "configdatatypeFilter", null, null, null, 3, 5, null, null, null);
    }
});