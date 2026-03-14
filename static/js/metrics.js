
document.querySelectorAll(".api-metric-chart").forEach(canvas => {
    // Parse the JSON strings into actual arrays
    const times = JSON.parse(canvas.dataset.times);
    const labels = JSON.parse(canvas.dataset.labels);

    new Chart(canvas, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Response Time (ms)",
                data: times,
                borderColor: "#00ff9c",
                backgroundColor: "rgba(0,255,156,0.2)",
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            mainAspectRatio: true,
            plugins: {
                tooltip: { mode: 'index', intersect:false},
                legend: { labels: { color: "#fff"} }
            },
            scales: {
                x: { 
                    grid: { color: "rgba(255,255,255,0.1)" }, 
                    ticks: { color: "#fff" } 
                },
                y: { 
                    grid: { color: "rgba(255,255,255,0.1)" }, 
                    ticks: { color: "#fff" } 
                }
            }
        }
    });
});
