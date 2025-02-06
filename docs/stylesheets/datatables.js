document.addEventListener("DOMContentLoaded", function () {
    function setupDataTable(tableId, unitsFilterId, dataTypeFilterId, powertrainFilterId, unitsColumn, dataTypeColumn, powertrainColumn) {
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
            uniqueValues.forEach(value => {
                let option = document.createElement("option");
                option.value = value;
                option.textContent = value;
                dropdown.appendChild(option);
            });
        }

        populateDropdown(unitsColumn, unitsFilterId);  // Units column
        populateDropdown(dataTypeColumn, dataTypeFilterId);  // Data Type column

        // Apply filtering based on dropdown selection
        function filterTable() {
            let unitsValue = document.getElementById(unitsFilterId).value.toLowerCase();
            let dataTypeValue = document.getElementById(dataTypeFilterId).value.toLowerCase();
            let powertrainValue = document.getElementById(powertrainFilterId).value.toLowerCase();

            table.rows().every(function () {
                let row = this.node();
                let rowUnits = row.cells[unitsColumn - 1].textContent.toLowerCase();
                let rowDataType = row.cells[dataTypeColumn - 1].textContent.toLowerCase();
                let rowPowertrain = row.cells[powertrainColumn - 1].textContent.toLowerCase();

                let matchUnits = unitsValue === "" || rowUnits === unitsValue;
                let matchDataType = dataTypeValue === "" || rowDataType === dataTypeValue;
                let matchPowertrain = powertrainValue === "" || rowPowertrain.includes(powertrainValue);

                if (matchUnits && matchDataType && matchPowertrain) {
                    this.nodes().to$().show();
                } else {
                    this.nodes().to$().hide();
                }
            });
        }

        document.getElementById(unitsFilterId).addEventListener("change", filterTable);
        document.getElementById(dataTypeFilterId).addEventListener("change", filterTable);
        document.getElementById(powertrainFilterId).addEventListener("change", filterTable);
    }

    // Initialize the vehicle parameters table
    if (document.getElementById("vehicleTable")) {
        setupDataTable("vehicleTable", "unitsFilter", "datatypeFilter", "powertrainFilter", 3, 6, 5);
    }

    // Initialize the scenario parameters table
    if (document.getElementById("scenarioTable")) {
        setupDataTable("scenarioTable", "scenarioUnitsFilter", "scenariodatatypeFilter", null, 3, 5, null);
    }

    // Initialize the ledger parameters table
    if (document.getElementById("ledgerTable")) {
        setupDataTable("ledgerTable", "ledgerUnitsFilter", "ledgerdatatypeFilter", "ledgercategoryFilter", 4, 6, 2);
    }

    // Initialize the config parameters table
    if (document.getElementById("configTable")) {
        setupDataTable("configTable", "configUnitsFilter", "configDataTypeFilter", null, 3, 5, null);
    }
});