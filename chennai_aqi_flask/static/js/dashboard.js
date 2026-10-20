// ======================================================
// Urban Air Quality Intelligence Platform
// Dashboard JavaScript
// ======================================================

let chart = null;

// ======================================================
// AQI GAUGE
// ======================================================

function updateGauge(aqi) {

    if (typeof Plotly === "undefined") return;

    let color = "#22c55e";

    if (aqi > 50) color = "#facc15";
    if (aqi > 100) color = "#fb923c";
    if (aqi > 200) color = "#ef4444";
    if (aqi > 300) color = "#7e22ce";

    Plotly.newPlot(
        "aqiGauge",
        [{
            type: "indicator",
            mode: "gauge+number",
            value: aqi,

            title: {
                text: "<b>Current AQI</b>"
            },

            number: {
                font: {
                    size: 42
                }
            },

            gauge: {

                axis: {
                    range: [0, 500]
                },

                bar: {
                    color: color,
                    thickness: 0.35
                },

                bgcolor: "white",
                borderWidth: 0,

                steps: [
                    { range: [0, 50], color: "#22c55e" },
                    { range: [50, 100], color: "#facc15" },
                    { range: [100, 200], color: "#fb923c" },
                    { range: [200, 300], color: "#ef4444" },
                    { range: [300, 500], color: "#7e22ce" }
                ]
            }

        }],

        {
            margin: {
                t: 20,
                b: 20,
                l: 30,
                r: 30
            }
        },

        {
            responsive: true,
            displayModeBar: false
        }
    );
}
// ======================================================
// AQI RECOMMENDATION
// ======================================================

function updateRecommendation(aqi) {

    const box = document.getElementById("recommendation");

    if (!box) return;

    let html = "";

    if (aqi <= 50) {

        html = `
            <li>😊 Air quality is Good.</li>
            <li>🏃 Outdoor activities are safe.</li>
            <li>💧 Stay hydrated.</li>
            <li>🌿 Enjoy fresh air.</li>
        `;

    }

    else if (aqi <= 100) {

        html = `
            <li>🙂 Air quality is Moderate.</li>
            <li>⚠ Sensitive individuals should limit prolonged outdoor exposure.</li>
            <li>😷 Carry a mask if required.</li>
            <li>💧 Drink enough water.</li>
        `;

    }

    else if (aqi <= 200) {

        html = `
            <li>⚠ Air quality is Poor.</li>
            <li>😷 Wear an N95 mask outdoors.</li>
            <li>🚶 Reduce outdoor activities.</li>
            <li>🏠 Keep windows closed.</li>
        `;

    }

    else if (aqi <= 300) {

        html = `
            <li>🚨 Air quality is Very Poor.</li>
            <li>🏠 Stay indoors whenever possible.</li>
            <li>😷 N95 mask is highly recommended.</li>
            <li>🚫 Avoid outdoor exercise.</li>
        `;

    }

    else {

        html = `
            <li>☠️ Air quality is Severe.</li>
            <li>🚫 Avoid going outdoors.</li>
            <li>🏠 Keep doors and windows closed.</li>
            <li>🩺 Follow medical advice if you have respiratory illness.</li>
        `;

    }

    box.innerHTML = html;

}
// ======================================================
// LOAD DASHBOARD DATA
// ======================================================

async function loadData() {

    const station = document.getElementById("station").value;

    try {

        const response = await fetch(`/api/live/${station}`);
        const data = await response.json();

        console.log("Dashboard API:", data);

        if (!response.ok || data.error) {
            alert(data.error || "Unable to load dashboard.");
            return;
        }

        // =================================================
        // TODAY AQI
        // =================================================

        document.getElementById("todayAQI").textContent =
            data.today_aqi;

        updateGauge(data.today_aqi);

        const todayCategory =
            document.getElementById("todayCategory");

        if (todayCategory) {

            todayCategory.textContent =
                data.today_category;

            todayCategory.style.color =
                data.today_color;

            todayCategory.style.fontWeight = "600";

        }

        // =================================================
        // FORECAST AQI
        // =================================================

        document.getElementById("forecastAQI").textContent =
            data.forecast_aqi;

        const forecastCategory =
            document.getElementById("forecastCategory");

        if (forecastCategory) {

            forecastCategory.textContent =
                data.forecast_category;

            forecastCategory.style.color =
                data.forecast_color;

            forecastCategory.style.fontWeight = "600";

        }

        // =================================================
        // HEALTH RISK
        // =================================================

        let risk = "LOW";

        if (data.forecast_aqi >= 300)
            risk = "VERY HIGH";
        else if (data.forecast_aqi >= 200)
            risk = "HIGH";
        else if (data.forecast_aqi >= 100)
            risk = "MEDIUM";

        document.getElementById("risk").textContent = risk;
                // =================================================
        // POLLUTANTS
        // =================================================

        document.getElementById("pm25").textContent =
            data.pollutants["PM2.5"];

        document.getElementById("pm10").textContent =
            data.pollutants["PM10"];

        document.getElementById("no2").textContent =
            data.pollutants["NO2"];

        document.getElementById("so2").textContent =
            data.pollutants["SO2"];

        document.getElementById("co").textContent =
            data.pollutants["CO"];

        // =================================================
        // WEATHER
        // =================================================

        if (document.getElementById("tempCard"))
            document.getElementById("tempCard").textContent =
                data.weather.temperature;

        if (document.getElementById("tempWeather"))
            document.getElementById("tempWeather").textContent =
                data.weather.temperature;

        document.getElementById("humidity").textContent =
            data.weather.humidity;

        document.getElementById("wind").textContent =
            data.weather.wind_speed;

        document.getElementById("pressure").textContent =
            data.weather.pressure;

        // =================================================
        // RECOMMENDATION
        // =================================================

        updateRecommendation(data.today_aqi);

        // =================================================
        // UPDATE AQI CHART
        // =================================================

        if (chart) {

            chart.data.labels = [
                "Yesterday",
                "Today",
                "Tomorrow"
            ];

            chart.data.datasets[0].data = [
                Math.max(data.today_aqi - 5, 0),
                data.today_aqi,
                data.forecast_aqi
            ];

            chart.update();
        }

    }

    catch (error) {

        console.error("Dashboard Error:", error);

        alert("Unable to load dashboard.");

    }

}
// ======================================================
// INITIALIZE DASHBOARD
// ======================================================

window.onload = function () {

    const canvas = document.getElementById("aqiChart");

    if (canvas) {

        const ctx = canvas.getContext("2d");

        if (chart) {
            chart.destroy();
        }

        chart = new Chart(ctx, {

            type: "line",

            data: {

                labels: [
                    "Yesterday",
                    "Today",
                    "Tomorrow"
                ],

                datasets: [

                    {

                        label: "Air Quality Index",

                        data: [0, 0, 0],

                        borderColor: "#2563eb",

                        backgroundColor: "rgba(37,99,235,0.15)",

                        borderWidth: 3,

                        fill: true,

                        tension: 0.4,

                        pointRadius: 6,

                        pointHoverRadius: 8,

                        pointBackgroundColor: "#2563eb",

                        pointBorderColor: "#ffffff",

                        pointBorderWidth: 2

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: true,

                animation: {
                    duration: 1200
                },

                interaction: {
                    mode: "index",
                    intersect: false
                },

                plugins: {

                    legend: {
                        display: true,
                        position: "top"
                    },

                    tooltip: {
                        enabled: true
                    }

                },

                scales: {

                    x: {

                        title: {
                            display: true,
                            text: "Timeline"
                        },

                        grid: {
                            display: false
                        }

                    },

                    y: {

                        beginAtZero: true,

                        suggestedMax: 500,

                        title: {
                            display: true,
                            text: "AQI"
                        },

                        ticks: {
                            stepSize: 50
                        }

                    }

                }

            }

        });

    }

    // Load dashboard automatically
    loadData();

};
// ======================================================
// GENERATE PERSONALIZED HEALTH REPORT
// ======================================================

async function generateHealthAdvice() {

    const station = document.getElementById("station").value;
    const age = parseInt(document.getElementById("age").value) || 25;
    const gender = document.getElementById("gender").value;
    const disease = document.getElementById("disease").value;
    const smoking = document.getElementById("smoking").value;

    try {

        const response = await fetch("/api/health", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                station,
                age,
                gender,
                disease,
                smoking
            })

        });

        const report = await response.json();

        console.log("Health Report:", report);

        if (!response.ok || report.error) {
            alert(report.error || "Unable to generate personalized health report.");
            return;
        }

        const summary = report.summary;
        const risk = report.risk;
        const advisory = report.advisory;

        // =================================================
        // RISK SUMMARY
        // =================================================

        if (document.getElementById("riskScore"))
            document.getElementById("riskScore").textContent =
                risk.risk_score;

        if (document.getElementById("riskLevel"))
            document.getElementById("riskLevel").textContent =
                risk.risk_level;

        if (document.getElementById("riskDescription"))
            document.getElementById("riskDescription").textContent =
                risk.message;

        // =================================================
        // RISK REASONS
        // =================================================

        const reasons = document.getElementById("riskReasons");

        if (reasons) {

            reasons.innerHTML = "";

            (advisory.why || []).forEach(item => {
                reasons.innerHTML += `<li>${item}</li>`;
            });

        }

        // =================================================
        // RECOMMENDATIONS
        // =================================================

        const recommendations =
            document.getElementById("recommendations");

        if (recommendations) {

            recommendations.innerHTML = "";

            [
                ...(advisory.personal || []),
                ...(advisory.weather || []),
                ...(advisory.forecast || []),
                ...(advisory.pollutants || []),
                ...(advisory.emergency || [])
            ].forEach(item => {

                recommendations.innerHTML += `<li>${item}</li>`;

            });

        }

    }

    catch (error) {

        console.error("Health Report Error:", error);

        alert("Unable to generate personalized health report.");

    }

}