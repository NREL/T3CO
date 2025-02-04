document.addEventListener("DOMContentLoaded", function () {
    let table = new DataTable("#vehicleTable", {
        paging: false,  // Show all rows
        searching: true, // Enable search
        ordering: true,  // Enable sorting
        info: false      // Hide table info
    });

    // Populate dropdowns with unique values
    function populateDropdown(columnIndex, dropdownId) {
        let uniqueValues = new Set();
        document.querySelectorAll(`#vehicleTable tbody tr td:nth-child(${columnIndex})`).forEach(cell => {
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

    populateDropdown(3, "unitsFilter");  // Units column (3rd index)
    populateDropdown(5, "dataTypeFilter");  // Data Type column (5th index)

    // Apply filtering based on dropdown selection
    function filterTable() {
        let unitsValue = document.getElementById("unitsFilter").value.toLowerCase();
        let dataTypeValue = document.getElementById("dataTypeFilter").value.toLowerCase();

        table.rows().every(function () {
            let row = this.node();
            let rowUnits = row.cells[2].textContent.toLowerCase();  // Units column
            let rowDataType = row.cells[4].textContent.toLowerCase(); // Data Type column

            let matchUnits = unitsValue === "" || rowUnits === unitsValue;
            let matchDataType = dataTypeValue === "" || rowDataType === dataTypeValue;

            if (matchUnits && matchDataType) {
                this.nodes().to$().show();
            } else {
                this.nodes().to$().hide();
            }
        });
    }

    document.getElementById("unitsFilter").addEventListener("change", filterTable);
    document.getElementById("dataTypeFilter").addEventListener("change", filterTable);
});
