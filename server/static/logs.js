const DATE_FORMAT = {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
};

function formatTimestamp(timestamp) {
    const date = new Date(timestamp.replace(" ", "T") + "Z");
    return isNaN(date) ? timestamp : date.toLocaleString([], DATE_FORMAT);
}

function createRow(log) {
    const row = document.createElement("tr");
    const cells = [
        formatTimestamp(log.timestamp),
        Number(log.temperature).toFixed(2),
        Number(log.humidity).toFixed(2),
        log.gas_value,
    ];
    cells.forEach((value, index) => {
        const cell = document.createElement("td");
        if (index > 0) {
            cell.className = "text-end";
        }
        cell.textContent = value;
        row.appendChild(cell);
    });
    return row;
}

function createEmptyRow() {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 4;
    cell.className = "text-center text-muted py-4";
    cell.textContent = "Sin registros";
    row.appendChild(cell);
    return row;
}

async function loadLogs() {
    const response = await fetch("/api/logs");
    const logs = await response.json();
    const body = document.getElementById("logs");
    body.replaceChildren(...(logs.length ? logs.map(createRow) : [createEmptyRow()]));
}

loadLogs();
