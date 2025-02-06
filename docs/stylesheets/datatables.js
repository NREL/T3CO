document.addEventListener("DOMContentLoaded", function () {
    function setupDataTable(tableId, categoryFilterId, unitsFilterId, dataTypeFilterId, categoryColumn, unitsColumn, dataTypeColumn) {
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

        populateDropdown(categoryColumn, categoryFilterId);  // Category column
        populateDropdown(unitsColumn, unitsFilterId);  // Units column
        populateDropdown(dataTypeColumn, dataTypeFilterId);  // Data Type column

        // Apply filtering based on dropdown selection
        function filterTable() {
            let categoryValue = document.getElementById(categoryFilterId).value.toLowerCase();
            let unitsValue = document.getElementById(unitsFilterId).value.toLowerCase();
            let dataTypeValue = document.getElementById(dataTypeFilterId).value.toLowerCase();

            table.rows().every(function () {
                let row = this.node();
                let rowCategory = row.cells[categoryColumn - 1].textContent.toLowerCase();  // Adjust for zero-based index
                let rowUnits = row.cells[unitsColumn - 1].textContent.toLowerCase();
                let rowDataType = row.cells[dataTypeColumn - 1].textContent.toLowerCase();

                let matchCategory = categoryValue === "" || rowCategory === categoryValue;
                let matchUnits = unitsValue === "" || rowUnits === unitsValue;
                let matchDataType = dataTypeValue === "" || rowDataType === dataTypeValue;

                if (matchCategory && matchUnits && matchDataType) {
                    this.nodes().to$().show();
                } else {
                    this.nodes().to$().hide();
                }
            });
        }

        document.getElementById(categoryFilterId).addEventListener("change", filterTable);
        document.getElementById(unitsFilterId).addEventListener("change", filterTable);
        document.getElementById(dataTypeFilterId).addEventListener("change", filterTable);
    }

    // Initialize the vehicle parameters table
    if (document.getElementById("vehicleTable")) {
        setupDataTable("vehicleTable", "unitsFilter", "dataTypeFilter", 2, 3, 5);
    }

    // Initialize the scenario parameters table
    if (document.getElementById("scenarioTable")) {
        setupDataTable("scenarioTable", "scenarioUnitsFilter", "scenarioDataTypeFilter", 2, 3, 5);
    }

    // Initialize the ledger parameters table
    if (document.getElementById("ledgerTable")) {
        setupDataTable("ledgerTable", "ledgercategoryFilter", "ledgerUnitsFilter", "ledgerdatatypeFilter", 2, 4, 6);
    }
});