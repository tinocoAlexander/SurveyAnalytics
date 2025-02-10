document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.querySelector('.search-input');
    const tableBody = document.querySelector('.surveys-table tbody');
    const paginationContainer = document.querySelector('.pagination');

    const allRows = Array.from(tableBody.querySelectorAll('tr'));
    const rowsPerPage = 5;
    let currentPage = 1;
    let filteredRows = allRows;

    function displayRows() {
        tableBody.innerHTML = ''; // Clear existing rows
        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const rowsToDisplay = filteredRows.slice(start, end);

        if (rowsToDisplay.length > 0) {
            rowsToDisplay.forEach(row => tableBody.appendChild(row));
        } else {
            // If no rows match, display a "no surveys found" row.
            const noRow = document.createElement('tr');
            const noDataTd = document.createElement('td');
            noDataTd.setAttribute('colspan', '4');
            noDataTd.textContent = 'No surveys found.';
            noRow.appendChild(noDataTd);
            tableBody.appendChild(noRow);
        }

        updatePagination();
    }

    function updatePagination() {
        paginationContainer.innerHTML = ''; // Clear existing buttons
        const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement('button');
            btn.classList.add('pagination-btn');
            btn.textContent = i;
            if (i === currentPage) {
                btn.classList.add('active');
            }
            btn.addEventListener('click', function() {
                currentPage = i;
                displayRows();
            });
            paginationContainer.appendChild(btn);
        }
    }

    searchInput.addEventListener('input', function() {
        const query = this.value.trim().toLowerCase();
        filteredRows = allRows.filter(row => {
            const surveyNameEl = row.querySelector('.survey-name');
            return surveyNameEl && surveyNameEl.textContent.toLowerCase().includes(query);
        });
        currentPage = 1;
        displayRows();
    });

    displayRows();
});