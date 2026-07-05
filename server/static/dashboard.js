let maxPoints = 0;

const INK_MUTED = "#898781";
const GRIDLINE = "#e1e0d9";

function createChart(canvasId, label, color) {
    return new Chart(document.getElementById(canvasId), {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: label,
                data: [],
                borderColor: color,
                backgroundColor: color + "22",
                borderWidth: 2,
                pointRadius: 2,
                pointHoverRadius: 5,
                tension: 0.3,
                fill: true,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            interaction: { mode: "index", intersect: false },
            plugins: {
                legend: { display: false },
                tooltip: { enabled: true },
            },
            scales: {
                x: { display: false },
                y: {
                    grid: { color: GRIDLINE },
                    ticks: { color: INK_MUTED },
                },
            },
        },
    });
}

const charts = {
    temperature: createChart("temperatureChart", "Temperatura", "#eb6834"),
    humidity: createChart("humidityChart", "Humedad", "#2a78d6"),
    gas_value: createChart("gasChart", "Gas", "#eda100"),
};

function formatTime(timestamp) {
    const date = new Date(timestamp.replace(" ", "T") + "Z");
    return isNaN(date) ? timestamp : date.toLocaleTimeString();
}

function seedChart(chart, labels, values) {
    chart.data.labels = labels;
    chart.data.datasets[0].data = values;
    chart.update();
}

function pushPoint(chart, value) {
    const dataset = chart.data.datasets[0];
    chart.data.labels.push(new Date().toLocaleTimeString());
    dataset.data.push(value);
    if (maxPoints && dataset.data.length > maxPoints) {
        chart.data.labels.shift();
        dataset.data.shift();
    }
    chart.update();
}

function renderStatus(data) {
    document.getElementById("temperature").textContent = Number(data.temperature).toFixed(2);
    document.getElementById("humidity").textContent = Number(data.humidity).toFixed(2);
    document.getElementById("gas_value").textContent = data.gas_value;
    const fan = document.getElementById("fan_on");
    fan.textContent = data.fan_on ? "ON" : "OFF";
    fan.className = "badge " + (data.fan_on ? "bg-success" : "bg-secondary");
}

async function loadHistory() {
    const response = await fetch("/api/readings");
    const { limit, readings } = await response.json();
    maxPoints = limit;
    if (!readings.length) {
        return;
    }
    const labels = readings.map((reading) => formatTime(reading.timestamp));
    seedChart(charts.temperature, labels.slice(), readings.map((reading) => Number(reading.temperature)));
    seedChart(charts.humidity, labels.slice(), readings.map((reading) => Number(reading.humidity)));
    seedChart(charts.gas_value, labels.slice(), readings.map((reading) => Number(reading.gas_value)));
    renderStatus(readings[readings.length - 1]);
}

function connect() {
    const ws = new WebSocket(`ws://${location.host}/ws`);
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        renderStatus(data);

        pushPoint(charts.temperature, Number(data.temperature));
        pushPoint(charts.humidity, Number(data.humidity));
        pushPoint(charts.gas_value, Number(data.gas_value));
    };
}

loadHistory().catch(console.error).then(connect);
