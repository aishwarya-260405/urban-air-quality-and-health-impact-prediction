console.log("Forecast JS Loaded!");

// ======================================================
// Urban Air Quality Intelligence Platform
// Forecast Page JavaScript
// ======================================================// ======================================================
// Urban Air Quality Intelligence Platform
// Forecast Page JavaScript
// ======================================================

let forecastChart = null;

// ------------------------------------------------------
// Load Forecast Data
// ------------------------------------------------------

async function loadForecast() {

    const stationSelect = document.getElementById("station");

    const station = stationSelect
        ? stationSelect.value
        : "Kodungaiyur";

    try {

        const response = await fetch(`/api/live/${station}`);

        const data = await response.json();

        if (!response.ok || data.error) {
            throw new Error(data.error || "Unable to fetch forecast.");
        }

        console.log("Forecast API:", data);

        console.log(data.next7);


        console.log("Confidence =", data.confidence);

        // -----------------------------
        // Values
        // -----------------------------

        const todayAQI = Number(data.today_aqi);

        const tomorrowAQI = Number(data.forecast_aqi);

        const difference = tomorrowAQI - todayAQI;

        const todayCategory =
            data.today_category || "Unknown";

        const todayColor =
            data.today_color || "#4C9A5B";

        const forecastCategory =
            data.forecast_category || "Unknown";

        const forecastColor =
            data.forecast_color || "#4C9A5B";

        const statement =
            data.forecast_message || "";

        const method =
            data.forecast_method || "Model";

        const history =
            data.history_days || "--";

        const next7 =
    data.next7 || [];

        const confidence = `${data.confidence}%`;

        // ------------------------------------
// AI Explanation
// ------------------------------------

const ai = data.ai_explanation || {};

const aiSummary =
    ai.summary || "No explanation available.";

const aiReasons =
    ai.reasons || [];

const featureImportance =
    ai.feature_importance || [];

        // -----------------------------
        // KPI Cards
        // -----------------------------

        document.getElementById("todayAQI").innerText =
            todayAQI;

        document.getElementById("forecastAQI").innerText =
            tomorrowAQI;

        document.getElementById("changeAQI").innerText =
            (difference >= 0 ? "+" : "") + difference;

        document.getElementById("confidence").innerText =
            confidence;

        const todayStatus =
            document.getElementById("todayStatus");

        if (todayStatus) {

            todayStatus.innerText = todayCategory;

            todayStatus.style.color = todayColor;

            todayStatus.style.fontWeight = "600";

        }

        const forecastStatus =
            document.getElementById("forecastStatus");

        if (forecastStatus) {

            forecastStatus.innerText = forecastCategory;

            forecastStatus.style.color = forecastColor;

            forecastStatus.style.fontWeight = "600";

        }

        const changeText =
            document.getElementById("changeText");

        if (changeText) {

            if (difference > 0) {

                changeText.innerText =
                    "AQI Expected to Increase";

            }

            else if (difference < 0) {

                changeText.innerText =
                    "AQI Expected to Improve";

            }

            else {

                changeText.innerText =
                    "No Significant Change";

            }

        }        // -----------------------------
        // Forecast Details
        // -----------------------------

        document.getElementById("todayDetail").innerText =
            todayAQI;

        document.getElementById("tomorrowDetail").innerText =
            tomorrowAQI;

        document.getElementById("differenceDetail").innerText =
            (difference >= 0 ? "+" : "") + difference;

        document.getElementById("categoryDetail").innerText =
            forecastCategory;

        document.getElementById("categoryDetail").style.color =
            forecastColor;

        document.getElementById("categoryDetail").style.fontWeight =
            "600";

        document.getElementById("confidenceDetail").innerText =
            confidence;

        const methodElement =
            document.getElementById("methodDetail");

        if (methodElement) {

            methodElement.innerText = method;

        }

        const historyElement =
            document.getElementById("historyDetail");

        if (historyElement) {

            historyElement.innerText =
                history + " Days";

        }

        // -----------------------------
        // AI Forecast Summary
        // -----------------------------

        const summary =
            document.getElementById("forecastSummary");

        if (summary) {

            summary.innerHTML = `

            <strong>Today's AQI:</strong>
            ${todayAQI}
            <br><br>

            <strong>Tomorrow's Predicted AQI:</strong>
            ${tomorrowAQI}
            <br><br>

            <strong>Expected Category:</strong>

            <span style="color:${forecastColor};
            font-weight:600;">

            ${forecastCategory}

            </span>

            <br><br>

            <strong>Health Impact:</strong>

            ${statement}

            <br><br>

            <strong>Prediction Method:</strong>

            ${method}

            <br><br>

            <strong>Historical Data Used:</strong>

            ${history} Days

            <br><br>

            <strong>Expected AQI Change:</strong>

            ${(difference >= 0 ? "+" : "") + difference}

            `;

        }

        // ------------------------------------
// Explainable AI
// ------------------------------------

const aiSummaryElement =
    document.getElementById("aiSummary");

if (aiSummaryElement) {

    aiSummaryElement.innerHTML =
        aiSummary;

}

// --------------------
// Reasons
// --------------------

const reasonBox =
    document.getElementById("aiReasons");

if (reasonBox) {

    reasonBox.innerHTML = "";

    aiReasons.forEach(reason => {

        const li =
            document.createElement("li");

        li.innerHTML =
            "✅ " + reason;

        li.style.marginBottom =
            "12px";

        reasonBox.appendChild(li);

    });

}

// --------------------
// Feature Importance
// --------------------

const featureBox =
    document.getElementById("featureImportance");

if (featureBox) {

    featureBox.innerHTML = "";

    featureImportance.forEach(item => {

        featureBox.innerHTML += `

        <div style="margin-bottom:18px;">

            <div style="
                display:flex;
                justify-content:space-between;
                margin-bottom:6px;
                font-weight:600;">

                <span>${item.feature}</span>

                <span>${item.weight}%</span>

            </div>

            <div style="
                width:100%;
                height:10px;
                background:#eef2ff;
                border-radius:20px;">

                <div style="
                    width:${item.weight}%;
                    height:10px;
                    border-radius:20px;
                    background:linear-gradient(90deg,#2563eb,#06b6d4);">

                </div>

            </div>

        </div>

        `;

    });

}


        // -----------------------------
// 7-Day Forecast Chart
// -----------------------------



const chartLabels = [

    "Today",

    "Day 1",

    "Day 2",

    "Day 3",

    "Day 4",

    "Day 5",

    "Day 6",

    "Day 7"

];

const chartValues = [

    todayAQI,

    ...next7.map(day => day.aqi)

];     

// Create / Refresh Chart
        // ------------------------------------

        if (forecastChart) {

            forecastChart.destroy();

        }

        const ctx = document
            .getElementById("forecastChart")
            .getContext("2d");


            const aqiBackground = {

    id: "aqiBackground",

    beforeDraw(chart) {

        const {

            ctx,

            chartArea,

            scales

        } = chart;

        if (!chartArea) return;

        const {

            left,

            right

        } = chartArea;

        function drawBand(min, max, color) {

            const y1 = scales.y.getPixelForValue(max);

            const y2 = scales.y.getPixelForValue(min);

            ctx.save();

            ctx.fillStyle = color;

            ctx.fillRect(

                left,

                y1,

                right - left,

                y2 - y1

            );

            ctx.restore();

        }

        drawBand(0,50,"rgba(76,175,80,0.08)");

        drawBand(50,100,"rgba(255,235,59,0.08)");

        drawBand(100,200,"rgba(255,152,0,0.08)");

        drawBand(200,300,"rgba(244,67,54,0.08)");

        drawBand(300,400,"rgba(156,39,176,0.08)");

        drawBand(400,500,"rgba(97,97,97,0.08)");

    }

};
forecastChart = new Chart(ctx, {

    type: "line",

    data: {

        labels: chartLabels,

        datasets: [{

            label: "AI Forecast",

            data: chartValues,

            borderColor: "#2563eb",

            backgroundColor: "rgba(37,99,235,0.15)",

            pointBackgroundColor: "#2563eb",

            pointBorderColor: "#ffffff",

            pointBorderWidth: 2,

            pointRadius: 5,

            pointHoverRadius: 10,

            borderWidth: 4,

            fill: true,

            tension: 0.35

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        plugins: {

            legend: {

                display: true,

                position: "top"

            },

            tooltip: {

                mode: "index",

                intersect: false,

                callbacks: {

                    title: function(context) {

                        return context[0].label;

                    },

                    label: function(context) {

                        return `Predicted AQI: ${context.parsed.y}`;

                    },

                    afterLabel: function(context) {

                        const value = context.parsed.y;

                        if (value <= 50) return "🟢 Good";
                        if (value <= 100) return "🟡 Satisfactory";
                        if (value <= 200) return "🟠 Moderate";
                        if (value <= 300) return "🔴 Poor";
                        if (value <= 400) return "🟣 Very Poor";

                        return "⚫ Severe";

                    }

                }

            }

        },

        interaction: {

            mode: "nearest",

            intersect: false

        },

        scales: {

    y: {

        beginAtZero: true,

        max: 500,

        ticks: {

            stepSize: 50

        },

        title: {

            display: true,

            text: "Air Quality Index"

        },

        grid: {

            color: "#dfe6ef"

        }

    },

    x: {

        title: {

            display: true,

            text: "Forecast Timeline"

        }

    }

}
    },

    plugins: [

        aqiBackground

    ]

});


// -------------------------------------
// Dynamic AI Recommendations
// -------------------------------------

const recommendationBox =
    document.getElementById("forecastRecommendations");

if (recommendationBox) {

    recommendationBox.innerHTML = "";

    let cards = [];

    if (tomorrowAQI <= 50) {

        cards = [

            {
                icon: "🏃",
                title: "Outdoor Exercise",
                message: "Excellent air quality is expected. Walking, jogging and cycling are recommended."
            },

            {
                icon: "🌳",
                title: "Enjoy Outdoor Activities",
                message: "This is a great day for parks and outdoor recreation."
            },

            {
                icon: "😌",
                title: "Low Health Risk",
                message: "Air pollution is unlikely to affect healthy individuals."
            }

        ];

    }

    else if (tomorrowAQI <= 100) {

        cards = [

            {
                icon: "🚶",
                title: "Normal Activities",
                message: "Most outdoor activities are safe, but avoid heavy traffic areas."
            },

            {
                icon: "💧",
                title: "Stay Hydrated",
                message: "Drink enough water while spending time outdoors."
            },

            {
                icon: "🌤",
                title: "Moderate Air Quality",
                message: "Sensitive individuals should monitor symptoms if spending long periods outside."
            }

        ];

    }

    else if (tomorrowAQI <= 200) {

        cards = [

            {
                icon: "😷",
                title: "Wear N95 Mask",
                message: "Consider wearing an N95 mask during outdoor travel."
            },

            {
                icon: "🚗",
                title: "Avoid Traffic",
                message: "Reduce exposure near busy roads and congested areas."
            },

            {
                icon: "🫁",
                title: "Sensitive Groups",
                message: "People with asthma or heart disease should reduce prolonged outdoor exposure."
            }

        ];

    }

    else {

        cards = [

            {
                icon: "🏠",
                title: "Stay Indoors",
                message: "Poor air quality is expected. Avoid unnecessary outdoor exposure."
            },

            {
                icon: "😷",
                title: "Protect Yourself",
                message: "Wear a certified N95 mask if outdoor travel is unavoidable."
            },

            {
                icon: "❤️",
                title: "Health Alert",
                message: "Children, older adults and people with respiratory or heart disease should remain indoors."
            }

        ];

    }

    cards.forEach(card => {

        recommendationBox.innerHTML += `

        <div class="tip-card">

            <div class="tip-icon">

                ${card.icon}

            </div>

            <div class="tip-content">

                <h4>${card.title}</h4>

                <p>${card.message}</p>

            </div>

        </div>

        `;

    });

}


// -------------------------------------
// 7-Day Forecast Table
// -------------------------------------

const table = document.getElementById("forecastTable");

if (table) {

    table.innerHTML = "";

    next7.forEach((day, index) => {

        let category = "";

        if (day.aqi <= 50)
            category = "🟢 Good";
        else if (day.aqi <= 100)
            category = "🟡 Satisfactory";
        else if (day.aqi <= 200)
            category = "🟠 Moderate";
        else if (day.aqi <= 300)
            category = "🔴 Poor";
        else if (day.aqi <= 400)
            category = "🟣 Very Poor";
        else
            category = "⚫ Severe";

        table.innerHTML += `
            <tr>
                <td style="padding:12px;">Day ${index + 1}</td>
                <td>${day.aqi}</td>
                <td>${category}</td>
            </tr>
        `;

    });

}

    }

    catch (error) {

        console.error("Forecast Error:", error);

        alert("Unable to load forecast.");

    }

}

// ------------------------------------------------------
// Initialize Page
// ------------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {

    loadForecast();

    const station = document.getElementById("station");

    if (station) {

        station.addEventListener("change", loadForecast);

    }

});
