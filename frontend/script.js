let impactChart = null;
function analyzeDecision() {
    const decision = document.getElementById("decisionSelect").value;
    const frequency = document.getElementById("frequency").value;
    const time_period = document.getElementById("time_period").value;
    const dreamJob = document.getElementById("dreamJob").value;

    // Validation
    if (!decision) {
        alert("Please select a decision first.");
        return;
    }

    if (!dreamJob) {
        alert("Please enter your dream job.");
        return;
    }
    
    if (!frequency || !time_period) {
        alert("Please enter frequency (hours) and time period (days).");
        return;
    }    

    // Backend API call
    fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            decision_id: decision,
            frequency: frequency,
            time_period: time_period,
            dream_job: dreamJob
        })        
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Backend response error");
        }
        return response.json();
    })
    .then(data => {
        // Show result container
        document.getElementById("result").style.display = "block";

        document.getElementById("capability").innerText =
            "Capability: " + data.capability_percent + "%";

        document.getElementById("advice").innerText =
                "Advice: " + data.advice;

        // Pattern
        document.getElementById("pattern").innerText = data.pattern;

        // Butterfly effect impact formatting
        let impactText = "";
        for (const key in data.butterfly_effect) {
            impactText += `${key.toUpperCase()}: ${data.butterfly_effect[key]}  `;
        }
        document.getElementById("impact").innerText = impactText;

        // Explanation
        document.getElementById("explanation").innerText = data.explanation;

        // Dream Job Analysis (Harsh / Reverse Psychology)
        document.getElementById("dreamAnalysis").innerText =
            `${data.advice} (Capability Score: ${data.capability_score})`;

        document.getElementById("butterflyIntensity").innerText =
        data.butterfly_intensity;
        
        // -------- GRAPH CODE START --------

        // Labels and values from backend
        const labels = Object.keys(data.butterfly_effect);
        const values = Object.values(data.butterfly_effect);

        // Destroy old chart if it exists
        if (impactChart) {
            impactChart.destroy();
        }

        // Get canvas context
        const ctx = document.getElementById("impactChart").getContext("2d");
        const backgroundColors = values.map(v => v >= 0 ? "rgba(0, 200, 0, 0.6)" : "rgba(200,0,0,0.6)");

        // Create bar chart
        impactChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Impact Score",
                    data: values,
                    backgroundColor: backgroundColors
                }]
            },
            options: { 
                responsive: true, 
                scales: { 
                    y: { 
                        beginAtZero: true } 
                    } 
                }
        });

        // -------- GRAPH CODE END --------

    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error connecting to backend. Make sure server is running.");
    });
}