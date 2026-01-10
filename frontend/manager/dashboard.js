// Call Volume
new Chart(document.getElementById("callVolume"), {
  type: "bar",
  data: {
    labels: ["Oct", "Nov", "Dec", "Jan"],
    datasets: [
      {
        label: "Inbound",
        data: [120, 180, 140, 220],
        backgroundColor: "#8b5cf6"
      },
      {
        label: "Outbound",
        data: [80, 120, 100, 180],
        backgroundColor: "#c4b5fd"
      }
    ]
  }
});

// Handle Time
new Chart(document.getElementById("handleTime"), {
  type: "line",
  data: {
    labels: ["Oct", "Nov", "Dec", "Jan"],
    datasets: [{
      label: "Avg Time",
      data: [80, 150, 220, 300],
      borderColor: "#10b981",
      fill: false
    }]
  }
});

// Sentiment
new Chart(document.getElementById("sentiment"), {
  type: "bar",
  data: {
    labels: ["Positive", "Neutral", "Negative"],
    datasets: [{
      data: [5490, 2490, 4825],
      backgroundColor: ["#10b981", "#a5b4fc", "#7c3aed"]
    }]
  },
  options: {
    indexAxis: "y"
  }
});
