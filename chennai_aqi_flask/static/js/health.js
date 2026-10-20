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
        console.log(report);

        console.log("PERSONAL =", report.advisory.personal);

        if (report.error) {

            alert(report.error);

            return;

        }

        //-------------------------------------------------
// Shortcuts
//-------------------------------------------------

const summary = report.summary;
const risk = report.risk;
const advisory = report.advisory;


//-------------------------------------------------
// Dynamic AI Tip Cards
//-------------------------------------------------

const tipsContainer = document.getElementById("dynamicTips");

tipsContainer.innerHTML = "";

advisory.tips.forEach(tip => {

    tipsContainer.innerHTML += `

    <div class="tip-card">

        <div class="tip-icon">
            ${tip.icon}
        </div>

        <div class="tip-content">

            <h4>${tip.title}</h4>

            <p>${tip.message}</p>

        </div>

    </div>

    `;

});
        //-------------------------------------------------
        // KPI Cards
        //-------------------------------------------------

        document.getElementById("riskAQI").innerHTML =
            summary.current_aqi;

        document.getElementById("forecastAQI").innerHTML =
            summary.forecast_aqi;

        document.getElementById("riskScore").innerHTML =
            risk.risk_score;

        document.getElementById("gaugeScore").innerHTML =
    risk.risk_score;

document.getElementById("gaugeLevel").innerHTML =
    risk.risk_level;

        document.getElementById("riskLevel").innerHTML =
            risk.risk_level;

        document.getElementById("exposureLevel").innerHTML =
            risk.exposure_level;

       const primary =
    advisory.pollutants.find(p => p.primary_pollutant);

document.getElementById("primaryPollutant").textContent =
    primary ? primary.primary_pollutant : "N/A";


    //-------------------------------------------------
// AI Health Impact Analysis
//-------------------------------------------------

const analysis = document.getElementById("healthAnalysis");

analysis.innerHTML = "";

let concern = "General Wellness";
let reason = "";
let severity = risk.risk_level;

if (disease === "Asthma") {

    concern = "Respiratory System";

    reason =
        "Because you have Asthma, today's air quality can trigger breathing discomfort. Outdoor exposure should be limited during polluted periods.";

}

else if (disease === "COPD") {

    concern = "Respiratory System";

    reason =
        "COPD increases sensitivity to pollutants. Your lungs are expected to experience greater stress than healthy individuals.";

}

else if (disease === "Heart Disease") {

    concern = "Cardiovascular System";

    reason =
        "Heart Disease makes you more vulnerable to pollution-related cardiovascular stress, especially during outdoor activity.";

}

else if (age >= 60) {

    concern = "Senior Health";

    reason =
        "Older adults are naturally more vulnerable to air pollution because lung capacity and immunity gradually decline.";

}

else if (age < 18) {

    concern = "Child Protection";

    reason =
        "Children have developing lungs and breathe faster than adults, making them more sensitive to polluted air.";

}

else {

    concern = "Preventive Health";

    reason =
        "No major personal health risks were detected. Continue monitoring daily AQI before outdoor activities.";

}

analysis.innerHTML = `

<div class="analysis-card">

    <div class="analysis-header">

        🧠 ${concern}

        <span class="severity-badge">
            ${severity}
        </span>

    </div>

    <div class="analysis-body">

        <p>${reason}</p>

        <div class="analysis-stats">

    <div class="stat-box">

        <span>AQI</span>

        <h3>${summary.current_aqi}</h3>

    </div>

    <div class="stat-box">

        <span>Forecast</span>

        <h3>${summary.forecast_aqi}</h3>

    </div>

    <div class="stat-box">

        <span>Exposure</span>

        <h3>${risk.exposure_level}</h3>

    </div>

</div>

    </div>

</div>

`;
        
        //-------------------------------------------------
        // Why This Result?
        //-------------------------------------------------

        const reasonList =
            document.getElementById("riskReasons");

        reasonList.innerHTML = "";

        advisory.why.forEach(item => {

            const li = document.createElement("li");

            li.innerHTML = item;

            reasonList.appendChild(li);

        });
                //-------------------------------------------------
        // Personal Advice
        //-------------------------------------------------

        const recommendationList =
            document.getElementById("recommendations");

        recommendationList.innerHTML = "";

        advisory.personal.forEach(item => {

            const li = document.createElement("li");

            li.innerHTML = item.message;

            recommendationList.appendChild(li);

        });
                //-------------------------------------------------
        // Weather Insights
        //-------------------------------------------------

        const weatherList =
            document.getElementById("weatherInsights");

        weatherList.innerHTML = "";

        advisory.weather.forEach(item => {

            const li = document.createElement("li");

            li.innerHTML = item.title
                ? `<b>${item.title}</b>: ${item.message}`
                : item.message;

            weatherList.appendChild(li);

        });

        //-------------------------------------------------
        // Forecast Insights
        //-------------------------------------------------

        const forecastList =
            document.getElementById("forecastInsights");

        forecastList.innerHTML = "";

        advisory.forecast.forEach(item => {

            const li = document.createElement("li");

            li.innerHTML = item.title
                ? `<b>${item.title}</b>: ${item.message}`
                : item.message;

            forecastList.appendChild(li);

        });

        //-------------------------------------------------
        // Pollutant Insights
        //-------------------------------------------------

        const pollutantList =
            document.getElementById("pollutantInsights");

        pollutantList.innerHTML = "";

        advisory.pollutants.forEach(item => {

            if (item.primary_pollutant) return;

            const li = document.createElement("li");

            li.innerHTML = item.message;

            pollutantList.appendChild(li);

        });

    //-------------------------------------------------
// Scroll to Result
//-------------------------------------------------

document.getElementById("healthResult").scrollIntoView({

    behavior: "smooth"

});

}

catch (err) {

    console.error(err);

    alert("Unable to generate personalized health report.");

}

}