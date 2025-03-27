document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("prediction-form").addEventListener("submit", function(event) {
        event.preventDefault();
        
        const data = {
            temperature: parseFloat(document.getElementById("temperature").value),
            co2_emissions: parseFloat(document.getElementById("co2").value),
            sea_level_rise: parseFloat(document.getElementById("sea_level").value),
            precipitation: parseFloat(document.getElementById("precipitation").value),
            humidity: parseFloat(document.getElementById("humidity").value),
            wind_speed: parseFloat(document.getElementById("wind_speed").value)
        };

        fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById("result").innerHTML = `
                <h3>Climate Risk Index: ${result.climate_risk_index}</h3>
                <p>${result.risk_level}</p>
                <h3>Weather Severity Index: ${result.weather_severity_index}</h3>
                <p>${result.severity}</p>
            `;
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("result").innerHTML = "<p style='color:red;'>Failed to fetch predictions. Please try again.</p>";
        });
    });
});
